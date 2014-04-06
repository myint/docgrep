#!/usr/bin/env python

"""Setup for docgrep."""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import ast

from setuptools import setup


def version():
    """Return version string."""
    with open('docgrep.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


with open('README.rst') as readme:
    setup(name='docgrep',
          version=version(),
          description='Like grep, but searches for matches in docstrings.',
          long_description=readme.read(),
          license='Expat License',
          author='Steven Myint',
          url='https://github.com/myint/docgrep',
          classifiers=['Intended Audience :: Developers',
                       'Environment :: Console',
                       'Programming Language :: Python :: 2.7',
                       'Programming Language :: Python :: 3',
                       'Programming Language :: Python :: 3.4',
                       'License :: OSI Approved :: MIT License'],
          keywords='grep, search, docstrings',
          py_modules=['docgrep'],
          entry_points={'console_scripts': ['docgrep = docgrep:main']})
