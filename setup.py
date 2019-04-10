#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Setup for PyPI usage."""

import sys
from glob import glob
from setuptools import setup

def get_long_description():
    """Get the package's long description."""
    with open("README.md", "r") as ifstrm:
        return ifstrm.read()

def get_version():
    """Get the package's version from without using an import."""
    with open("src/enrichmentanalysis/__init__.py", "r") as ifstrm:
        for line in ifstrm:
            if line[:15] == "__version__ = '":
                return line.rstrip()[15:-1]

def get_install_requires():
    """Get requirements for installation."""
    # pip: User installs items in requirements.txt
    base = ['docopt', 'xlsxwriter']
    # conda: Anaconda installs all needed to run scripts
    if sys.argv[1:2] == ['bdist_conda']:
        base.append('statsmodels')
    return base


setup(
    name='enrichmentanalysis_dvklopfenstein',
    version=get_version(),
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
    install_requires=get_install_requires(),
)
