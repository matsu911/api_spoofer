# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import re

def preprocess_file(filename, cpp_path='cpp', cpp_args=''):
    path_list = [cpp_path]
    if isinstance(cpp_args, list):
        path_list += cpp_args
    elif cpp_args != '': 
        path_list += [cpp_args]
    path_list += [filename]

    try:
        pipe = Popen(path_list, stdout=PIPE, universal_newlines=True)
        text = pipe.communicate()[0]
    except OSError as e:
        raise RuntimeError("Unable to invoke 'cpp'.  " +
            'Make sure its path was passed correctly\n' +
            ('Original error: %s' % e))

    return text

def remove_comments(s):
    return "\n".join([x for x in s.split('\n') if len(x) and x[0] != '#'])

def strip(str_list):
    return [x.strip() for x in str_list]

def _extract_function_declares(file):
    functions = []
    matcher = re.compile("(?:extern\s+)?(\w+)\s+(\w+)\s*\(([^)]*)\)")
    for m in [x for x in map(matcher.match, strip(remove_comments(preprocess_file(file)).split(';'))) if x]:
        functions.append([m.group(1), m.group(2), strip(m.group(3).split(','))])
    return functions

def extract_function_declares(*filenames):
    return reduce(list.__add__, map(_extract_function_declares, filenames))
