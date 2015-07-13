# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/
# python.exe -m doctest  stackFrame.py # stackFrame.py is argv to doctest.script
# from __future__ import print_function
import argparse
import diGuiXiaJian
import unittest

import re
import functools
PREFIX = ''
def trace(fn):
    """A decorator that prints a function's name, its arguments, and its return
    values each time the function is called. For example,

    @trace
    def compute_something(x, y):
        # function body
    """
    @functools.wraps(fn)
    def wrapped(*args, **kwds):
        global PREFIX
        reprs = [repr(e) for e in args] 
        reprs += [repr(k) + '=' + repr(v) for k, v in kwds.items()]
        log('{0}({1})'.format(fn.__name__, ', '.join(reprs)) + ':')
        PREFIX += '    '
        try:
            result = fn(*args, **kwds)
            PREFIX = PREFIX[:-4]
        except Exception as e:
            log(fn.__name__ + ' exited via exception')
            PREFIX = PREFIX[:-4]
            raise
        # Here, print out the return value.
        #log('{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result))
        log('-> {0}'.format(result,))
        return result
    return wrapped
    
def log(message):
    """Print an indented message (used with trace)."""
    if type(message) is not str:
        message = str(message)
    print(PREFIX + re.sub('\n', '\n' + PREFIX, message))

isa = isinstance

class TestCName(unittest.TestCase):
    def setUp(self):
        # Perform set up actions (if any)
        print('\nsetUp called')
        pass
    def tearDown(self):
        # Perform clean-up actions (if any)
        print('tearDown', 'called')
        pass
                
    def testXXX(self):
        print('testXXX', 'called')
    def yacc(self):
        print('yacc', 'called')     
    pass

if __name__ == "__main__":
        unittest.main()