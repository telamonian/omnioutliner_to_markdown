#!/usr/bin/env python
from setuptools import find_packages, setup

package_dir = {'': 'src/python',
               'ootomd': 'src/python/ootomd'}

setup(
    author = 'Max Klein',
    description = 'Package for helping to convert OmniOutliner files and share them online.',
    # entry_points={'console_scripts': ['autofocus_analyze = robertslab.cnn_autofocus.bin.autofocus_analyze:main',},
    license = 'Apache License, Version 2.0',
    name = 'omnioutliner_to_markdown',
    package_dir = package_dir,
    packages = find_packages(where='./src/python'),    #, exclude=('setupUtils', 'robertslab.test', 'robertslab.test.*')),
    #scripts = ['robertslab/md/src/rmsd/spark/rmsdSpark.py']
)