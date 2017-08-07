'''

  ponywhoosh
  ~~~~~~~~~~

  Make your database over PonyORM searchable.

  :copyright: (c) 2015-2017 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''

from __future__              import absolute_import
from __future__              import division
from __future__              import print_function

import os
import re
import sys
import whoosh

from collections             import defaultdict
from .index                  import Index  as PonyWhooshIndex
from pony                    import orm
from pony.orm.serialization  import to_dict
from pprint                  import pprint
from whoosh                  import fields as whoosh_module_fields
from whoosh                  import index  as whoosh_module_index
from whoosh                  import qparser

__all__   = ['PonyWhoosh']
basedir   = os.path.abspath(os.path.dirname(__file__))


class PonyWhoosh(object):

  """A top level class that allows to register indexes and performing searches.

  Attributes:
      * debug (bool): print some messages useful for debugging
      * indexes_path (str): this is the name where the folder of the indexes
        are going to be stored.
      * search_string_min_len (int): let you config the minimun string value
        possible to perform search.
      * writer_timeout (int): a time constraint for running a search process.
  """

  debug                 = False
  indexes_path          = 'indexes'
  search_string_min_len = 2
  writer_timeout        = 2

  _indexes              = {}
  _entities             = {}

  def __init__(self):
    if not os.path.exists(self.indexes_path):
      os.makedirs(self.indexes_path)


  def delete_indexes(self):
    """This set to empty all the indexes registered.
    """
    self._indexes = {}

  def indexes(self):
    """Access a list of the current indexes registered

    Returns:
        (list): the indexes stored.
    """
    return [v for k, v in list(self._indexes.items())]

  def create_index(self, index):
    """Creates and opens index folder for given index.
    If the index already exists, it just opens it, otherwise it creates it first.
    """

    index._path = os.path.join(self.indexes_path, index._name)

    if whoosh.index.exists_in(index._path):
      _whoosh = whoosh.index.open_dir(index._path)
    elif not os.path.exists(index._path):
      os.makedirs(index._path)
      _whoosh = whoosh.index.create_in(index._path, index._schema)
    index._whoosh = _whoosh

  def register_index(self, index):
    """Registers a given index:

    * Creates and opens an index for it (if it doesn't exist yet)
    * Sets some default values on it (unless they're already set)

    Args:
        index (PonyWhoosh.Index): An instance of PonyWhoosh.Index class
    """

    self._indexes[index._name] = index
    self.create_index(index)
    return index

  def register_model(self, *fields, **kw):
    """Registers a single model for fulltext search. This basically creates
    a simple PonyWhoosh.Index for the model and calls self.register_index on it.

    Args:
        *fields: all the fields indexed from the model.
        **kw: The options for each field, sortedby, stored ...
    """

    index         = PonyWhooshIndex(pw=self)
    index._kw     = kw
    index._fields = fields

    def inner(model):
      """This look for the types of each field registered in the index,
      whether if it is Numeric, datetime, boolean or just text.

      Args:
          model (PonyORM.Entity): A model defined on the database with PonyORM

      Returns:
          model (PonyORM.Entity): A model modified for handle the appropriate
          search methods.
      """

      index._name = model._table_
      if not index._name:
        index._name  = model.__name__

      self._entities[index._name]     = model
      index._schema_attrs             = {}
      index._primary_key_is_composite = model._pk_is_composite_
      index._primary_key              = [f.name for f in model._pk_attrs_]
      index._primary_key_type         = 'list'
      type_attribute                  = {}

      for field in model._attrs_:
        if field.is_relation:
          continue

        assert hasattr(field, "name") and hasattr(field, "py_type")

        fname = field.name
        if hasattr(field.name, "__name__"):
            fname = field.name.__name__

        stored = kw.get("stored", False)
        if fname in index._primary_key:
            kw["stored"] = True
        # we're not supporting this kind of data
        ftype = field.py_type.__name__
        if ftype in ['date', 'datetime', 'datetime.date']:
            kw["stored"] = stored
            continue

        fwhoosh = fwhoosh = whoosh.fields.TEXT(**kw)

        if field == model._pk_:
            index._primary_key_type = ftype
            fwhoosh = whoosh.fields.ID(stored=True, unique=True)

        if fname in index._fields:
          if not field.is_string:
            if ftype in ['int', 'float']:
              fwhoosh = whoosh.fields.NUMERIC(**kw)
            elif ftype == 'bool':
              fwhoosh = whoosh.fields.BOOLEAN(stored=True)

        type_attribute[fname]      = ftype
        index._schema_attrs[fname] = fwhoosh
        kw["stored"]               = stored

      index._schema = whoosh.fields.Schema(**index._schema_attrs)

      self.register_index(index)

      def _middle_save_(obj, status):
        """A middle-in-middle method to intercept CRUD operations from PonyORM
        over the current object model to update the appropriate whoosh index.

        Args:
            obj (EntityInstance): An instance of a current model.
            status (str): Type of transaction on the database. A CRUD operation.

        Returns:
            obj (EntityInstance): The same object as the input.
        """

        writer   = index._whoosh.writer(timeout=self.writer_timeout)
        dict_obj = obj.to_dict()

        def dumps(v):
          if sys.version_info[0] < 3:
            if isinstance(v, int):
              return unicode(v)
            if isinstance(v, float):
              return '%.9f' % v
            return unicode(v)
          else:
            if isinstance(v, int):
              return str(v)
            if isinstance(v, float):
              return int(float(v))
            return str(v)

        attrs = {}
        if sys.version_info[0] < 3:
          for k, v in dict_obj.iteritems():
            if k in index._schema_attrs.keys():
              attrs[k] = dumps(v)
        else:
          for k, v in dict_obj.items():
            if k in list(index._schema_attrs.keys()):
              attrs[k] = dumps(v)

        if status == 'inserted':
          writer.add_document(**attrs)
        elif status == 'updated':
          writer.update_document(**attrs)
        elif status in set(['marked_to_delete', 'deleted', 'cancelled']):
          writer.delete_by_term(primary, attrs[primary])

        writer.commit()
        return obj._after_save_

      index._model       = model
      model._after_save_ = _middle_save_
      model._pw_index_   = index
      model.search       =  model._pw_index_.search
      return model
    return inner

  @orm.db_session
  def search(self, *arg, **kw):
    """A full search function. This allows you to search expression
    using the following arguments.

    Arg:
        query (str): The search string expression.

    Optional Args:
        - include_entity (bool): include in each result the entity values associated of the fields stored.
        - add_wildcards (bool): set it if you want to consider matches that have prefix or suffixes the query.
        - something (bool): set `add_willcards` in case of none results for the query.
        - fields (list): specified the fields names that you want to consider.
        - except_fields (list): specified the fields names to not consider in the search.
        - models (list): a list of name of model to search or even the models from the database.

    Returns:
        (dict): A python dictionary with the results.
    """
    output = {
        'cant_results'  : 0
      , 'matched_terms' : defaultdict(set)
      , 'results'       : {}
      , 'runtime'       : 0
    }

    indexes = self.indexes()

    models = kw.get('models', list(self._entities.values()))
    if sys.version_info[0] < 3:
      models = [self._entities.get(model, None) if isinstance(model, str)
        or isinstance(model, unicode) else model for model in models]
      models = filter(lambda x: x is not None, models)
    else:
      models = [self._entities.get(model, None) if isinstance(model, str)
        or isinstance(model, str) else model for model in models]
      models = [x for x in models if x is not None]


    if models == [] or not models:
      models = list(self._entities.values())

    if self.debug:
      print("SEARCHING ON MODELS -> ", models)

    indexes = [m._pw_index_ for m in models if hasattr(m, '_pw_index_')]

    if indexes == []:
      return output

    runtime, cant = 0, 0
    ma            = defaultdict(set)

    for index in indexes:
      res     = index.search(*arg, **kw)
      runtime += res['runtime']
      cant    += res['cant_results']
      if res['cant_results'] > 0:
        output['results'][index._name] = {
            'items'         : res['results']
          , 'matched_terms' : res['matched_terms']
        }
        for k, ts in list(res['matched_terms'].items()):
          for t in ts:
            ma[k].add(t)

    output['cant_results']  = cant
    output['matched_terms'] = {k: list(v) for k, v in list(ma.items())}
    output['runtime']       = runtime
    return output
