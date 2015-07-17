# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/ 
# http://www.jianshu.com/p/250f0d305c35
# http://pyzh.readthedocs.org/en/latest/Descriptor-HOW-TO-Guide.html
# http://stackoverflow.com/questions/13007179/python-data-and-non-data-descriptors

# python.exe -m doctest  descriptor.py # descriptor.py is argv to doctest.script
# %run descriptor.py

'''
>>> PythonSite.webframework
'Flask'
>>> PythonSite.webframework = 'Tornado'
>>> PythonSite.webframework
'Tornado'


'''
# from __future__ import print_function
import inspect
import sys
import pprint
import functools
import argparse
import re
###############################
# Descriptor attribute for an integer type-checked attribute
#http://python3-cookbook.readthedocs.org/zh_CN/latest/c08/p09_create_new_kind_of_class_or_instance_attribute.html
class Integer:
    def __init__(self, name):
        self.name = name



    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]
class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y


class WebFramework(object):
    def __init__(self, name='Flask'):
        self.name = name

    def __get__(self, instance, owner):
        return self.name

    def __set__(self, instance, value):
        self.name = value


class PythonSite(object):

    webframework = WebFramework()

#只有__get__的描述符，在查找field时，优先级低于实例字典    
#http://stackoverflow.com/questions/13007179/python-data-and-non-data-descriptors
class Descriptor(object):
    def __init__(self, name):
        self.name = name
    def __get__(self, instance, cls):
        print ('Getting %s, with instance %r, class %r' % (self.name, instance, cls))
    
class Foo(object):
    desc = Descriptor('Class-stored descriptor')
class Foo(object):
    _spam = 'eggs'
    @property
    def spam(self):
        return self._spam
    @spam.setter
    def spam(self, val):
        self._spam = val
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

    if len(sys.argv) > 1 :_test(sys.argv[1])
       
    import doctest
    doctest.testmod() 