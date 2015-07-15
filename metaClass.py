# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/
# python.exe -m doctest  stackFrame.py # stackFrame.py is argv to doctest.script
# from __future__ import print_function

#pycon.b0.upaiyun.com/.../shell909090-meta-class.htm 元编程是一种黑魔法，正派人士都很畏惧。——张教主
class Meta(type):
    def __init__(cls, name, bases, attrs):
        output = attrs['output']#局部变量output 等于class构造时的method函数output
        attrs['output'] = lambda self, x: output(self, 'python')#通过元类，把method函数output彻底给改了
        return type.__new__(cls, name, bases, attrs)

class Base(dict,metaclass = Meta):#如果用python2写法，在3下面不工作    不报错
    def output(self, o): 
        print ('hello, %s' % o)
b = Base()
b.output('world')

#http://openhome.cc/Gossip/Python/Metaclass.html
class SomeMeta(type):#这里仅仅是伪代码说明__new__和__init__被调用顺序，你绝对不应该重写元类的__call__
    def __call__(definedclz, *args, **kwargs):
        print('__new__')
        instance = definedclz.__new__(definedclz, *args, **kwargs)
        print('__init__')
        definedclz.__init__(instance, *args, **kwargs)
        return instance
class Some(metaclass=SomeMeta):#Some=SomeMeta(,,    )
    def __new__(clz):
        print('Some __new__')
        return object.__new__(clz)
    def __init__(self):
        print('Some __init__')
s = Some()    