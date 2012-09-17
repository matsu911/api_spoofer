#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from api_spoofer import extract_function_declares

for f in extract_function_declares('/usr/include/stdio.h'):
    print f
