'''

  ponywhoosh
  ~~~~~~~~~~

  Your database now searchable.

  :copyright: (c) 2015-2017 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
  :license: BSD (see LICENSE.md)

'''

from __future__             import absolute_import, print_function

import io
import os
import re

from glob                   import glob
from os.path                import basename, dirname, join, relpath, splitext
from setuptools             import find_packages, setup


def read(*names, **kwargs):
  return io.open(
      join(dirname(__file__), *names),
      encoding=kwargs.get('encoding', 'utf8')
  ).read()

setup(
  , name='ponywhoosh'
  , version="1.7.1"
  , url='https://github.com/compiteing/ponywhoosh'
  , license='MIT'
  , author='Jonathan Prieto-Cubides & Felipe Rodriguez'
  , author_email='jprieto9@eafit.edu.co'
  , description='Your database now searchable. The backend behind the Flask-PonyWhoosh.'
  , long_description='%s\n%s' % (
      read('README.rst'), re.sub(':obj:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst')))
  , packages=find_packages()
  , zip_safe=False
  , include_package_data=True
  , platforms='any'
  , keywords=
    [ 'elastic'
    , 'engine'
    , 'flask'
    , 'flask-sqlalchemy'
    , 'flask-whooshalchemy'
    , 'mysql'
    , 'pony'
    , 'ponyorm'
    , 'ponywhoosh'
    , 'search'
    , 'searchable'
    , 'sqlite3'
    , 'whoosh'
    ]
  , install_requires=['pony', 'whoosh']
  , classifiers=[
      'Environment :: Web Environment'
    , 'Intended Audience :: Developers'
    , 'License :: OSI Approved :: BSD License'
    , 'Operating System :: OS Independent'
    , 'Programming Language :: Python'
    , 'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    , 'Topic :: Software Development :: Libraries :: Python Modules'
  ]
)

# pandoc --from=rst --to=rst --output=README.rst README.rst
# Pasos para subir a pypi
# git tag v...
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
