#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

dependencies = [
  'docopt',
  'gitpython',
  'google-api-python-client'
]

setup(
  name='genpub',
  version='0.0.1',
  description='genpub',
  url='',
  license='MIT License',
  author='Anders Hoff',
  author_email='inconvergent@gmail.com',
  install_requires=dependencies,
  packages=[
    'genpub'
  ],
  entry_points={
    'console_scripts': [
      'genpub=genpub:run'
    ]
  },
  zip_safe=True
)

