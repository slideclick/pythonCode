# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/
# python.exe -m doctest  stackFrame.py # stackFrame.py is argv to doctest.script
# from __future__ import print_function
'''
a=A()
a()会失败，因为class A没有定义__call__
class A写__call__为了a()因为a是A的实例
class type写__call__为了A()因为A是type的实例
所以class type一定有__call__（元类是type的派生可以override基类的__call__但是一般不用）

class type的__call__干什么呢？
class type写__call__为了A()
A()就是调用class type的__call__
它调用A的__new__生成a这个东东
然后传递a这个东东给A.__init__
A的__new__的入口参数是A这个东东
a=A()时A这个东东已经有了，调用__new__入口参数就是A

那么A这个东东怎么来的？
答：class A定义时，就是 A=type()
A()就是class type的__call__
type()就是class Type的__call__
它调用type的__new__生成A这个东东
type的__new__的入口参数是type这个东东

>>> ds = DictSorted()
>>> d = {}
>>> ds['a'] = 1
>>> ds['b'] = 2
>>> ds.setdefault('c', 3)
3
>>> d['a'] = 1
>>> d['b'] = 2
>>> d.setdefault('c', 3)
3
'''
#pycon.b0.upaiyun.com/.../shell909090-meta-class.htm 元编程是一种黑魔法，正派人士都很畏惧。——张教主
class Meta(type):
    def __new__(cls, name, bases, attrs):#这个函数名字换成 __init__ 试试 cls传入参数就变了
        print(cls.__base__,cls,type(name))#<class 'type'> <class '__main__.Meta'>,name现在是个str还不是东东
        output = attrs['output']#局部变量output 等于class构造时的method函数output
        attrs['output'] = lambda self, x: output(self, 'python')#通过元类，把method函数output彻底给改了
        return super().__new__(cls, name, bases, attrs)#type

class Base(dict,metaclass = Meta):#如果用python2写法，在3下面不工作    不报错
    def output(self, o): 
        print ('hello, %s' % o)
b = Base()
b.output('world')

#http://openhome.cc/Gossip/Python/Metaclass.html
class SomeMeta(type):#这里仅仅是伪代码说明__new__和__init__被调用顺序，你绝对不应该重写元类的__call__
    def __call__(definedclz, *args, **kwargs):
        print(definedclz)#<class '__main__.Some'>
        print('__new__')
        instance = definedclz.__new__(definedclz, *args, **kwargs)
        print('__init__')
        definedclz.__init__(instance, *args, **kwargs)
        return instance
class Some(metaclass=SomeMeta):#Some=SomeMeta(,,    )
    def __new__(clz):#<class '__main__.Some'>
        print(clz)
        print('Some __new__')
        return object.__new__(clz)
    def __init__(self):
        print(self)#<__main__.Some object at 0x00000000033CEC50>
        print('Some __init__')
s = Some()    

# %run metaClass.py 下面这个例子取自应该 python00第6章是的dict被打印时key是有序的
class Edge(tuple):
    '''这个都要缩进？
    重载new必须得返回一个实例回来，一般你应该调用super
    '''
    def __new__(cls, e1, e2):
        return tuple.__new__(cls, (e1, e2))
    def __repr__(self):
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))
    __str__ = __repr__
    
from collections import KeysView, ItemsView, ValuesView
class DictSorted(dict,metaclass = type):
    def __new__(cls, *args, **kwargs):
        #print(cls)
        new_dict = dict.__new__(cls, *args, **kwargs)
        new_dict.ordered_keys = []
        return new_dict

    def __setitem__(self, key, value):
        '''self[key] = value syntax'''
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        super().__setitem__(key, value)

    def setdefault(self, key, value):
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        return super().setdefault(key, value)

    def keys(self):
        return KeysView(self)

    def values(self):
        return ValuesView(self)

    def items(self):
        return ItemsView(self)

    def __iter__(self):
        '''for x in self syntax'''
        return self.ordered_keys.__iter__()
        
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()