# -*- coding: utf-8 -*-

from extract import extract_function_declares, preprocess_file
from pyELF import get_symbol_names
from optparse import OptionParser
import os

def main():
    usage = "usage: %prog [options] bin_path"
    parser = OptionParser(usage=usage, version="%prog 0.0.1")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    bin_path = args[0]
    if not os.path.exists(bin_path):
        parser.error("%s does not exist" % bin_path)

    header_files = ['/usr/include/stdio.h', '/usr/include/stdlib.h', '/usr/include/time.h']
    funcs = extract_function_declares(*header_files)
    syms = get_symbol_names(bin_path)

    print "#define _GNU_SOURCE 1"
    print "#include <dlfcn.h>"
    for header in map(os.path.basename, header_files):
        print "#include <%s>" % header
    print

    for ret_type, fun_name, args in funcs:
        args = filter(lambda x: x[0] != 'void', args)
        if fun_name in syms:
            for i in xrange(0, len(args)):
                if not args[i][1]:
                    args[i][1] = 'arg%d' % i
            if ret_type == 'void':
                print """void %s(%s)
{
  typedef void (*ftype)(%s);
  ((ftype)dlsym(RTLD_NEXT, "%s"))(%s);
}
""" % (fun_name, ", ".join([" ".join(x) for x in args]), ", ".join([x[0] for x in args]), fun_name, ", ".join([x[1] for x in args]))
            else:
                print """%s %s(%s)
{
  typedef %s (*ftype)(%s);
  return ((ftype)dlsym(RTLD_NEXT, "%s"))(%s);
}
""" % (ret_type, fun_name, ", ".join([" ".join(x) for x in args]), ret_type, ", ".join([x[0] for x in args]), fun_name, ", ".join([x[1] for x in args]))

