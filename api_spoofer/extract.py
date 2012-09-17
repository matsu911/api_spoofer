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

def strip(arg):
    if type(arg) is list:
        return [x and x.strip() for x in arg]
    else:
        return arg.strip()

def split_into_type_and_name(s):
    m = re.compile("^(.*?)(\w+)?$").match(s.strip())
    if len(m.group(1)) == 0:
        return strip([m.group(2), None])
    else:
        return strip([m.group(1), m.group(2)])

def _extract_function_declares(file):
    functions = []
    matcher = re.compile("(?:extern\s+)?((?:\w+\s+)|(?:\w+\s*\**\s*))(\w+)\s*\(([^)]*)\)")
    for m in [x for x in map(matcher.match, strip(remove_comments(preprocess_file(file)).split(';'))) if x]:
        if m.group(1).strip() != 'typedef':
            functions.append([m.group(1).strip(), m.group(2).strip(), map(split_into_type_and_name, m.group(3).split(','))])
    return functions

def extract_function_declares(*filenames):
    return reduce(list.__add__, map(_extract_function_declares, filenames))
