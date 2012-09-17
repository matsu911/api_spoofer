#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from test_function import TestFunctions

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestFunctions))
    return suite
