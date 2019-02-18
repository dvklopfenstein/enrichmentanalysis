#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Setup for PyPI usage."""

import os.path as op

from glob import glob
from setuptools import setup


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]

SETUP_DIR = op.abspath(op.dirname(__file__))

setup(
    name='enrichmentanalysis',
    version=0.1,
    author='DV Klopfenstein',
    author_email='dvklopfenstein@gmail.com',
    license='MIT License',
    long_description='Code for generic enrichment analysis',
    packages=['enrichmentanalysis'],
    include_package_data=True,
    # package_data={"enrichmentanalysis.test_data": ["*.*"]},
    scripts=glob('src/bin/*.py'),
    classifiers=CLASSIFIERS,
    url='http://github.com/dvklopfenstein/enrichmentanalysis',
    description='Enrichment analysis',
    install_requires=['docopt', 'scipy', 'datetime', 'collections'],
)
