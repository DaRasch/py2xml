#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import re

try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

PROJECT_NAME = 'py2xml'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


### FIND ALL SUB-PACKAGES ###
def iter_packages(root):
    ignore = len(os.path.dirname(root)) + 1
    for path, _, files in os.walk(root):
        if '__init__.py' in files:
            yield '.'.join(path[ignore:].split(os.path.sep))
PACKAGES = list(iter_packages(os.path.join(ROOT_DIR, PROJECT_NAME)))


### METADATA ###
try:
    with open(os.path.join(ROOT_DIR, PROJECT_NAME, '__init__.py')) as f:
        VERSION = re.search("__version__ = '([^']+)'", f.read()).group(1)
except IOError:
    with open(os.path.join(ROOT_DIR, PROJECT_NAME + '.py')) as f:
        VERSION = re.search("__version__ = '([^']+)'", f.read()).group(1)

with open(os.path.join(ROOT_DIR, 'README.md')) as f:
    README = f.read()

with open(os.path.join(ROOT_DIR, 'LICENSE')) as f:
    LICENSE = f.read()

metadata = {
    'name': PROJECT_NAME,
    'version': VERSION,
    'description': "Magic declarative XML building tool.",
    'long_description': README,
    'author': 'Philipp Rasch',
    'author_email': 'ph.r@hotmail.de',
    #'url': '',
    #'download_url': '',
    'platforms': 'any',
    'license': LICENSE,
    'packages': PACKAGES,
    'classifiers': ('Intended Audience :: Developers',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Programming Language :: Python :: 3.5'
    )
}

# setuptools only arguments
if has_setuptools:
    metadata.update({
    #'tests_require': ['pytest>=2.6.1']
})


if __name__ == '__main__':
    setup(**metadata)
