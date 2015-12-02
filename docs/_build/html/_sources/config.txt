.. _config:

================
Getting Started:
================


Installation
************

.. code:: python

    pip install ponywhoosh

or

.. code:: bash

    git clone https://github.com/compiteing/PonyWhoosh.git



Configuration
**************



Initialize the
Ponywhoosh and set up the general configurations. 

.. code :: python
	
	from ponywhoosh import Ponywhoosh
	pw = Ponywhoosh() 

.. code:: python

    pw.search_string_min_len= 3
    pw.indexes_path='ponyindexes'
    pw.writer_timeout= 2



These configurations set up the default folder to save the Indexes, if you want to activate debug, the minimun lenght of the string in the query, the time out (stop searching if is taking so much). 


Database Configuration
**********************

|database|

Import the ponywhoosh library in the file you have the database entities.

.. code:: python

    from PonyWhoosh import PonyWhoosh
    pw = PonyWhoosh()

For each entity wrap it up with the decorator
``@pw.register_model(*args,**kw)``. Specifying what attributes would be searcheables. For example:

.. code:: python

    @pw.register_model('name','age', sortable=True,  stored=True)
    class User(db.Entity):
        _table_ = 'User'
        id = PrimaryKey(int, auto=True)
        name = Required(unicode)
        tipo = Optional(unicode)
        age = Optional(int)
        entries = Set("Entry")
        attributes = Set("Attributes")

As you could see in the previous example, you should declare as strings these fields where you want whoosh to store the searcheables (``name``, ``age``, etc.). All the parameters from whoosh are available, You just have to listed separating them with commas: sortable, stored, scored, etc. Refer to whoosh documentation for
further explanations on the application of these parameters.

 

Searching: for the first  time
******************************



In python view  (we are using bpython by the way) you can search using the "search()" function. Running our example, let us suppose  we are looking for the word "applied" in the model Department. After we run our example.py , we should follow the following steps:

|first|



.. |appconfig| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/images/flaskappconfig.gif?raw=true
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh

.. |database| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/images/databaseconfig.gif?raw=true
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh

.. |first| image:: https://github.com/compiteing/ponywhoosh/blob/master/images/example.gif?raw=true
   :target: https://pypi.python.org/pypi/PonyWhoosh

