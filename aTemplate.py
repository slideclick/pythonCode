# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/ 
# 

# python.exe -m doctest  aTemplate.py # aTemplate.py is argv to doctest.script
# %run aTemplate.py

'''
>>> 2
1
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

    for ln in open('tGraph.py',encoding='utf-8').readlines(): #latin-1   cp936
        pat = re.compile(r'\S+nodes\[(\d)\],nodes\[(\d)\]\S')
        mat=pat.search(ln)
        if mat:
            print('{0} {1}'.format(mat.group(1),mat.group(2)),sep='',end = '\r\n')
        pass      
    
if __name__ == "__main__":
    f= open('aTemplate.py')
    txt = f.read()
    lines = txt.split('\r\n')
    print([ ln for ln in (ln.strip() for ln in lines)])
    f.close()

    for ln in open('aTemplate.py'):
        pass# who close it?
    with open('aTemplate.py') as f:
        for ln in f.readlines():
            pass
    if len(sys.argv) > 1 :_test(sys.argv[1])
       
    import doctest,unittest
    doctest.testmod() 
    unittest.main()