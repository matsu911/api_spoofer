#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from test_function import *

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestFunctions))
    suite.addTests(unittest.makeSuite(TestExtractFunctionDeclares))
    suite.addTests(unittest.makeSuite(TestExtractFunctionDeclares_thread_db_h))
    suite.addTests(unittest.makeSuite(Test_split_into_type_and_name))
    return suite
