'''

    ponywhoosh
    ~~~~~~~~~~

    Make your database over PonyORM searchable.

    :copyright: (c) 2015-2016 by Jonathan S. Prieto & Ivan Felipe Rodriguez.
    :license: BSD (see LICENSE.md)

'''

from __future__ import absolute_import, print_function

from glob import glob
import os
from os.path import basename, dirname, join, relpath, splitext
import re

from ponywhoosh import __version__

import io
from setuptools import find_packages, setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

setup(
    name='ponywhoosh',
    version=__version__,
    url='https://github.com/compiteing/ponywhoosh',
    license='BSD',
    author='Jonathan S. Prieto. & Ivan Felipe Rodriguez',
    author_email='prieto.jona@gmail.com',
    description='Make your database over PonyORM searchable. The backend behind the Flask-PonyWhoosh.',
    long_description='%s\n%s' % (
        read('README.rst'), re.sub(':obj:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    packages=['ponywhoosh',],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    keywords=['ponyorm', 'whoosh', 'search', 'searchable', 'pony' 'full-text', 'engine', 'flask-ponywhoosh'],
    install_requires=['pony', 'whoosh'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)

# pandoc --from=rst --to=rst --output=README.rst README.rst
# Pasos para subir a pypi
# git tag v...
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
