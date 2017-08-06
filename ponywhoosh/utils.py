'''

  ponywhoosh
  ~~~~~~~~~~

  Makes your database over PonyORM searchable.

  :copyright: (c) 2015-2017 by Jonathan Prieto-Cubides & Felipe Rodriguez.
  :license: MIT (see LICENSE.md)

'''
from __future__  import absolute_import
from __future__  import division
from __future__  import print_function

from pony        import orm

@orm.db_session
def search(model, *arg, **kw):
  """Ponywhoosh function to perform searches on specific models.
  It takes up three arguments:

  Args:
    model (Model) or (str): Where you want to search, in which table.
    query (str): the string expression to search.

  Optional Args:
    - include_entity (bool): include in each result the entity values
      associatedof the fields stored.
    - add_wildcards (bool): set it if you want to consider matches that
      have prefix or suffixes the query.
    - something (bool): set `add_willcards` in case of none results
      for the query.
    - fields (list): specified the fields names that you want to consider.
    - except_fields (list): specified the fields names to not consider in
      the search.
    - models (list): a list of name of model to search or even the models
      from the database.

  Returns:
    (dict): A python dictionary with the results for the model.
  """
  return model._pw_index_.search(*arg, **kw)


@orm.db_session
def delete_field(model, *arg):
  """ It deletes an specific field stored in the index.

  Args:
    model (Model): The model from where you want to delete the specific field(s).
    *arg: field(s) of the model specified that will be removed.

  Returns:
    (list): a schemma of the model with the fields removed.
  """
  return model._pw_index_.delete_field(*arg)


def full_search(pw, *arg, **kw):
  """ This function search in every model registered.
  And portrays the result in a dictionary where the keys are the models.

  Args:
    pw (PonyWhoosh): This is where all the indexes are stored.
    An instance of PonyWhoosh class.
    query (str): the string expression to search.

  Optional Args:
    - include_entity (bool): include in each result the entity
      values associated of the fields stored.
    - add_wildcards (bool): set it if you want to consider matches
      that have prefix or suffixes the query.
    - something (bool): set `add_willcards` in case of none results
      for the query.
    - fields (list): specified the fields names that you want to consider.
    - except_fields (list): specified the fields names to not consider in
      the search.
    - models (list): a list of name of model to search or even the models
      from the database.

  Returns:
    (dict): A python dictionary with the results for the model.
  """
  return pw.search(*arg, **kw)
