'''

  ponywhoosh
  ~~~~~~~~~~

  Makes your database over PonyORM searchable.

  :copyright: (c) 2015-2017 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
  :license: BSD (see LICENSE.md)

'''

import os
import shutil
import tempfile

from pony.orm    import *
from ponywhoosh  import PonyWhoosh, search, full_search
from pprint      import pprint
from unittest    import TestCase


class BaseTestCases(object):

  class BaseTest(TestCase):
    def __init__(self, *args, **kwargs):
      super(BaseTestCases.BaseTest, self).__init__(*args, **kwargs)

    def setUp(self):
      self.pw               = PonyWhoosh()
      self.pw.indexes_path  = tempfile.mkdtemp()
      self.pw.debug         = False
      self.db               = Database()

      @self.pw.register_model('name', 'age', stored=True, sortable=True)
      class User(self.db.Entity):
        id         = PrimaryKey(int, auto=True)
        name       = Required(str)
        age        = Optional(int)
        attributes = Set('Attribute')

      @self.pw.register_model('weight', 'sport', 'name', stored=True, sortable=True)
      class Attribute(self.db.Entity):
        id      = PrimaryKey(int, auto=True)
        name    = Optional(str)
        user    = Optional("User")
        weight  = Required(str)
        sport   = Optional(str)

      self.db.bind('sqlite', ':memory:', create_db=True)
      self.db.generate_mapping(create_tables=True)
      self.User       = User
      self.Attribute  = Attribute

    @db_session
    def fixtures(self):
      self.u1 = self.User(name='jonathan', age='15')
      self.u2 = self.User(name='felipe', age='19')
      self.u3 = self.User(name='harol', age='16')
      self.u4 = self.User(name='felun', age='16')
      self.a1 = self.Attribute(
          name='felun'
        , user=self.u1
        , weight='80'
        , sport='tejo'
        )
      self.a2 = self.Attribute(
          name='galun'
        , user=self.u2
        , weight='75'
        , sport='lucha de felinas'
        )
      self.a3 = self.Attribute(
          name='ejote'
        , user=self.u3
        , weight='65'
        , sport='futbol shaulin'
        )

    def tearDown(self):
      shutil.rmtree(self.pw.indexes_path, ignore_errors=True)
      self.pw.delete_indexes()
      self.db.drop_all_tables(with_all_data=True)

    def test_search(self):
      self.fixtures()
      found = self.User._pw_index_.search('harol', include_entity=True)
      self.assertEqual(found['cant_results'], 1)
      self.assertEqual(self.u3.id, found['results'][0]['entity']['id'])

    def test_search_something(self):
      self.fixtures()
      found = self.User._pw_index_.search('har', something=True, include_entity=True)
      self.assertEqual(found['cant_results'], 1)

    def test_full_search_without_wildcards(self):
      self.fixtures()

      found = full_search(self.pw, "fel")
      self.assertEqual(found['cant_results'], 0)

    def test_full_search_with_wildcards(self):
      self.fixtures()

      found = full_search(self.pw, "fel"
        , add_wildcards=True
        , include_entity=True
        )
      self.assertEqual(found['cant_results'], 4)

    def test_fields(self):
      self.fixtures()
      results = full_search(self.pw, "felun"
        , include_entity=True
        , fields=["name"]
        )
      self.assertEqual(results['cant_results'], 2)

    def test_models(self):
      self.fixtures()
      results = full_search(self.pw, "felun"
        , include_entity=True
        , models=['User']
        )
      self.assertEqual(results['cant_results'], 1)

    def test_except_field(self):
      self.fixtures()
      results = full_search(self.pw, "felun", except_fields=["name"])
      self.assertEqual(results['cant_results'], 0)


class TestGeneral(BaseTestCases.BaseTest):

  def setUp(self):
    super(TestGeneral, self).setUp()
