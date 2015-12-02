.. _example:

Example:
========

|first|

We have used one of the available databases example from ponyorm, the universities. To run de example, you should go to the console and do:

.. code:: bash

	bpython 

Then import the example and using  pw.search() you will be able to perform a simple search. 

.. code:: python
	>>> from example import *
	>>> populate_database()
	>>> pw.search(smith)
	>>> {'cant_results': 1,
 		'matched_terms': {'name': ['smith']},
 		'results': {'Student': {'items': [{'docnum': 1L,
                                    'pk': (u'1',),
                                    'score': 2.252762968495368}],
                         'matched_terms': {'name': ['smith']}}},
 		'runtime': 0.001795053482055664}

.. |first| image:: https://github.com/compiteing/ponywhoosh/blob/master/images/example.gif?raw=true
   :target: https://pypi.python.org/pypi/Flask-PonyWhoosh
