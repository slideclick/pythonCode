#python -c "
from __future__ import print_function; 
import re;import sys;
datepat=re.compile(r'(\d+)[/-]?(\d+)[/-]?(\d+)\D'
                    r'([01][0-9]):([0-5][0-9])');
[print(datepat.sub(r'\2/\3/\1T\4:\5',ln) if datepat.search(ln) else '' )for ln in sys.stdin if ' ' in ln ]
#python pythonRegTemplate.py < log.txt


import pprint
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
        log('{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result))
        return result
    return wrapped

def log(message):
    """Print an indented message (used with trace)."""
    if type(message) is not str:
        message = str(message)
    print(PREFIX + re.sub('\n', '\n' + PREFIX, message))