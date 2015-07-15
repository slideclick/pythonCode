# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/
# python.exe -m doctest  stackFrame.py # stackFrame.py is argv to doctest.script
# from __future__ import print_function
class Meta(type):
    def __new__(cls, name, bases, attrs):
        output = attrs['output']#局部变量output 等于class构造时的method函数output
        attrs['output'] = lambda self, x: output(self, 'python')#通过元类，把method函数output彻底给改了
        return type.__new__(cls, name, bases, attrs)

class Base(dict,metaclass = Meta):#如果用python2写法，不工作    
    def output(self, o): 
        print ('hello, %s' % o)
b = Base()
b.output('world')
