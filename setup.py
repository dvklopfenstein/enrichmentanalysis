#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Setup for PyPI usage."""

from glob import glob
from setuptools import setup

def get_long_description():
    """Get the package's long description."""
    with open("README.md", "r") as fh:
        long_description = fh.read()

setup(
    name='enrichmentanalysis_dvklopfenstein',
    version='0.0.2',
    author='DV Klopfenstein',
    author_email='dvklopfenstein@gmail.com',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=[
        'enrichmentanalysis',
    ],
    package_dir={'enrichmentanalysis': 'src/enrichmentanalysis'},
    # include_package_data=True,
    # package_data={"enrichmentanalysis.test_data.nbt_3102": ["*.*"]},
    scripts=glob('src/bin/*.py'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Operating System :: OS Independent',
    ],
    url='http://github.com/dvklopfenstein/enrichmentanalysis',
    description='Perform enrichment analysis on any IDs and associations',
    install_requires=['datetime'],
)
