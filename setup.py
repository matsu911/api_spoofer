#!/usr/bin/env python
# -*- coding:utf-8

from setuptools import setup, find_packages
import sys

sys.path.append('./')
sys.path.append('./test')

setup(name = "API Spoofer",
      version = "0.0.1",
      packages = find_packages(),
      author = "Shigeaki Matsumura",
      author_email = "matsu911@gmail.com",
      description = "API Spoofing Tool",
      url = "https://github.com/matsu911/api_spoofer",
      license = "GPL",
      long_description = "README.md",
      keywords = "API spoofing",
      test_suite = 'test_main.suite',
      entry_points = {
        'console_scripts' : "api_spoofer = api_spoofer:main"
        }
      )
