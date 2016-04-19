#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='CapTest',
      version='0.1',
      description='Testing applications based on screen captures',
      author='Jonas Pfannschmidt',
      author_email='jonas.pfannschmidt@gmail.com',
      packages=find_packages(exclude=['test']),
      install_requires=['autopy', 'pillow'])
