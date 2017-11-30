#!/usr/bin/env python
from setuptools import find_packages, setup

package_dir = {'': 'src/python',
               'todo_share': 'src/python/todo_share'}

setup(
    author = 'Max Klein',
    description = 'Package for helping to share todo lists online.',
    # entry_points={'console_scripts': ['autofocus_analyze = robertslab.cnn_autofocus.bin.autofocus_analyze:main',},
    license = 'Apache License, Version 2.0',
    name = 'todo_share',
    package_dir = package_dir,
    packages = find_packages(where='./src/python'),    #, exclude=('setupUtils', 'robertslab.test', 'robertslab.test.*')),
    #scripts = ['robertslab/md/src/rmsd/spark/rmsdSpark.py']
)