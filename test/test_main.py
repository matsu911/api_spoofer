#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from test_function import TestFunctions, TestExtractFunctionDeclares

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestFunctions))
    suite.addTests(unittest.makeSuite(TestExtractFunctionDeclares))
    return suite
