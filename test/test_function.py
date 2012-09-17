# -*- coding: utf-8 -*-

import unittest
from api_spoofer import extract_function_declares, get_symbol_names

class TestFunctions(unittest.TestCase):
    def test_extract_function_declares(self):
        funcs = extract_function_declares('/usr/include/stdio.h', '/usr/include/stdlib.h')
        self.assertTrue(['void *', 'malloc', ['size_t __size']] in funcs)
        self.assertTrue(['size_t', 'fread', ['void *__restrict __ptr', 'size_t __size', 'size_t __n', 'FILE *__restrict __stream']] in funcs)
        self.assertTrue(['size_t', 'fwrite', ['__const void *__restrict __ptr', 'size_t __size', 'size_t __n', 'FILE *__restrict __s']] in 
                        funcs)
        
    def test_get_symbol_names(self):
        syms = get_symbol_names('/bin/date')
        self.assertTrue('clock_settime' in syms)
