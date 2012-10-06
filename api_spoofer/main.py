# -*- coding: utf-8 -*-

from extract import extract_function_declares, preprocess_file
from pyELF import get_symbol_names
from optparse import OptionParser
import os, re
from glob import glob
from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE

def extract_header_files_by_symbols(syms, header_files):
    tmp = []
    for header_file in header_files:
        try:
            if set(syms).intersection(set(map(lambda x: x[1], extract_function_declares(header_file)))):
                tmp.append(header_file)
        except RuntimeError, e:
            continue
    return tmp
    
def extract_valid_header_files(syms, defines, include_dirs):
    header_files = extract_header_files_by_symbols(syms, reduce(list.__add__, [glob("%s/*.h" % x) for x in include_dirs]))

    try:
        while True:
            includes = ["#include <%s>" % os.path.basename(x) for x in header_files]

            tmp = NamedTemporaryFile(suffix='.c', delete=False)
            for line in defines:
                tmp.write(line + "\n")
            for line in includes:
                tmp.write(line + "\n")
            tmp.close()

            # pipe = Popen(['cpp', tmp.name], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            pipe = Popen(['gcc', '-c', '-o', '/dev/null', tmp.name], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            text = pipe.communicate()[1]
            matcher = re.compile("^(.*?):\d+:?(?:\d+:)?(?: error:)? ")
            for l in text.split('\n'):
                m = matcher.match(l)
                if m and m.group(1) and m.group(1) in header_files:
                    header_files.remove(m.group(1))
            matcher = re.compile(".* from (.*?):\d+")
            for l in text.split('\n'):
                m = matcher.match(l)
                if m and m.group(1) and m.group(1) in header_files:
                    header_files.remove(m.group(1))
            if pipe.returncode == 0:
                break
    except OSError as e:
        raise RuntimeError("Unable to invoke 'gcc'.  " +
            'Make sure its path was passed correctly\n' +
            ('Original error: %s' % e))
    os.unlink(tmp.name)

    return header_files

ignored_symbols = ['calloc']

def main():
    usage = "usage: %prog [options] bin_path"
    parser = OptionParser(usage=usage, version="%prog 0.0.1")
    parser.add_option("-I", dest="include_dirs", action="append", default=['/usr/include'],
                      help="include directories", metavar="DIR")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    bin_path = args[0]
    if not os.path.exists(bin_path):
        parser.error("%s does not exist" % bin_path)

    defines = []
    defines.append("#define _GNU_SOURCE 1")

    syms = get_symbol_names(bin_path)
    header_files = extract_valid_header_files(syms, defines, options.include_dirs)

    includes = []
    includes.append("#include <dlfcn.h>")
    for header in map(os.path.basename, header_files):
        includes.append("#include <%s>" % header)

    funcs = extract_function_declares(*header_files)

    lines = []
    for sym in [x for x in syms if x not in ignored_symbols]:
        for ret_type, fun_name, args in filter(lambda x: x[1] == sym, funcs):
            args = filter(lambda x: x[0] != 'void', args)
            for i in xrange(0, len(args)):
                if not args[i][1]:
                    args[i][1] = 'arg%d' % i
            if ret_type == 'void':
                lines.append("""void %s(%s)
{
  typedef void (*ftype)(%s);
  ((ftype)dlsym(RTLD_NEXT, "%s"))(%s);
}
""" % (fun_name, ", ".join([" ".join(x) for x in args]), ", ".join([x[0] for x in args]), fun_name, ", ".join([x[1] for x in args])))
            else:
                lines.append("""%s %s(%s)
{
  typedef %s (*ftype)(%s);
  return ((ftype)dlsym(RTLD_NEXT, "%s"))(%s);
}
""" % (ret_type, fun_name, ", ".join([" ".join(x) for x in args]), ret_type, ", ".join([x[0] for x in args]), fun_name, ", ".join([x[1] for x in args])))
            break

    for line in defines:
        print line
    print
    for line in includes:
        print line
    print
    for line in lines:
        print line

