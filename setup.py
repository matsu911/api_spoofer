#!/usr/bin/env python
# -*- coding:utf-8

from setuptools import setup, find_packages
import sys

sys.path.append('./')
sys.path.append('./test')

setup(name = "API Spoofer",
      version = "0.0.1",
      packages = find_packages(),
      test_suite = 'test_main.suite'
      )
