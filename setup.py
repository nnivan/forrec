#!/usr/bin/env python3

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='ForRec',
      version='0.0.1alpha',
      description='Forensic reconstruction tool for (Linux) machines',
      author='Ivan Nikolov',
      license="GPLv3",
      long_description=read('README.md'),
      url='https://github.com/nnivan/lh_project2018/',
      install_requires=['pexpect', 'python-vagrant', 'paramiko'],
      scripts=['scripts/forreconstruct.py'],
      packages=['forrec'],
     )
