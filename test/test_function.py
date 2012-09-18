# -*- coding: utf-8 -*-

import unittest
from api_spoofer import extract_function_declares, get_symbol_names

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
