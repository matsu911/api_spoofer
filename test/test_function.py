# -*- coding: utf-8 -*-

import unittest
from api_spoofer import extract_function_declares, get_symbol_names, split_into_type_and_name

class TestExtractFunctionDeclares_thread_db_h(unittest.TestCase):
    def test_therad_db_h(self):
        self.funcs = extract_function_declares('/usr/include/thread_db.h')

class TestExtractFunctionDeclares(unittest.TestCase):
    def setUp(self):
        self.funcs = extract_function_declares('/usr/include/stdio.h', '/usr/include/stdlib.h')

    def test_malloc(self):
        self.assertTrue(['void *', 'malloc', [['size_t', '__size']]] in self.funcs)

    def test_fread(self):
        self.assertTrue(['size_t', 'fread', [['void *__restrict', '__ptr'], 
                                             ['size_t', '__size'], 
                                             ['size_t', '__n'], 
                                             ['FILE *__restrict', '__stream']]] in self.funcs)

    def test_fwrite(self):
        self.assertTrue(['size_t', 'fwrite', [['__const void *__restrict', '__ptr'], 
                                              ['size_t', '__size'],
                                              ['size_t', '__n'],
                                              ['FILE *__restrict', '__s']]] in self.funcs)

    def test___overflow(self):
        self.assertTrue(['int', '__overflow', [['_IO_FILE *', None],
                                               ['int', None]]] in self.funcs)
        
class TestFunctions(unittest.TestCase):
    def test_get_symbol_names(self):
        syms = get_symbol_names('/bin/date')
        self.assertTrue('clock_settime' in syms)

class Test_split_into_type_and_name(unittest.TestCase):
    def test_1(self):
        self.assertEqual(['__const pthread_attr_t *__restrict', '__attr'],
                         split_into_type_and_name("""__const pthread_attr_t *__restrict 
__attr"""))

    def test_2(self):
        self.assertEqual(['__const pthread_mutexattr_t *      __restrict', '__attr'],
                         split_into_type_and_name("""__const pthread_mutexattr_t *
      __restrict __attr"""))

        
