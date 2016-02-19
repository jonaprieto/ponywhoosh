.. _config:

===============
Getting Started
===============


Installation
************

.. code:: python

    pip install ponywhoosh

or

.. code:: bash

    git clone https://github.com/compiteing/PonyWhoosh.git



PonyWhoosh Configuration
************************



Initialize the ``Ponywhoosh`` object and if you want, set up some general configurations. 

.. code :: python
	
	from ponywhoosh import Ponywhoosh
	pw = PonyWhoosh() 

.. code:: python

    pw.search_string_min_len= 3
    pw.indexes_path='ponyindexes'
    pw.writer_timeout= 2



These configurations set up the default folder to save the `Indexes`, if you want to activate debug, the minimun length of the string in the query, the time out (stop searching if is taking so much). 


Database Configuration
**********************



Import ``ponywhoosh`` in your source code where you have the database entities definitions.


|database|


As we show above, the lines will be look like these:


.. code:: python

    from PonyWhoosh import PonyWhoosh
    pw = PonyWhoosh()

For each entity wrap it up with the decorator
``@pw.register_model(...)``. Specifying what attributes would be searcheables. 

For example:

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

As you could see in the previous example, you should declare as `strings` these fields where you want search in the future and make them searcheables (``name``, ``age``, etc.). All the parameters from ``whoosh`` are available, You just have to listed separating them with commas: ``sortable``, ``stored``, ``scored``, etc. Refer to ``whoosh`` documentation for further explanations on the application of these parameters.



.. |appconfig| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/images/flaskappconfig.gif?raw=true
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh

.. |database| image:: https://github.com/compiteing/flask-ponywhoosh/blob/master/images/databaseconfig.gif?raw=true
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh

