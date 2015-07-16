# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/ 
# 

# python.exe -m doctest  aTemplate.py # aTemplate.py is argv to doctest.script
# %run aTemplate.py

'''
>>> 

'''
# from __future__ import print_function
import inspect
import sys
import pprint
import functools
import argparse
import re
###############################





###############################
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
        log('{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result))
        return result
    return wrapped

def log(message):
    """Print an indented message (used with trace)."""
    if type(message) is not str:
        message = str(message)
    print(PREFIX + re.sub('\n', '\n' + PREFIX, message))

#@trace
def _test(fname='null'):
    print('{0} calledBy {1}'.format(inspect.stack()[0][3],inspect.stack()[1][3])) 
    pass    
    
if __name__ == "__main__":
    for ln in open('aTemplate.py'):
        pass
    if len(sys.argv) > 1 :_test(sys.argv[1])
       
    import doctest
    doctest.testmod() 