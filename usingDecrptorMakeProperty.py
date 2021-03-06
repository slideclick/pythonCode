# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/ http://openhome.cc/Gossip/Python/Descriptor.html
# python.exe -m doctest  stackFrame.py # stackFrame.py is argv to doctest.script
# from __future__ import print_function

# http://openhome.cc/Gossip/Python/Descriptor.html

import inspect

def prop(getter, setter=None,deleter=None):#这不就是个构造函数么？使用了闭包
    class PropDesc:
        def __get__(self, instance, owner):
            return getter(instance)
            
        def __set__(self, instance, value):
            self.__setter(instance, value)
            
        def __delete__(self, instance):
            self.__deleter(instance)
            
        def deleter(self, deleter):
            self.__deleter = deleter
            return self        
            
        def setter(self, setter):
            self.__setter = setter
            return self   
            
    return PropDesc()
class Ball:
    def __init__(self, radius):
        if radius <= 0:
            raise ValueError('必須是正數')
        self.__radius = radius
    
    def getRadius(self):
        print('{0} calledBy {1}'.format(inspect.stack()[0][3],inspect.stack()[1][3]))
        return self.__radius
        
    def setRadius(self, radius):
        print('{0} calledBy {1}'.format(inspect.stack()[0][3],inspect.stack()[1][3]))
        self.__radius = radius
        
    def delRadius(self):
        print('{0} calledBy {1}'.format(inspect.stack()[0][3],inspect.stack()[1][3]))
        del self.__radius
        
    radius = prop(getRadius, setRadius, delRadius)    
    
class ABall:
    def __init__(self, radius):
        if radius <= 0:
            raise ValueError('必須是正數')
        self.__radius = radius
    
    @prop
    def radius(self):
        print('{0} calledBy {1}'.format(inspect.stack()[0][3],inspect.stack()[1][3]))
        return self.__radius
        
    @radius.deleter    
    def delRadius(self):
        print('{0} calledBy {1}'.format(inspect.stack()[0][3],inspect.stack()[1][3]))
        del self.__radius     
        
    @radius.setter    
    def setRadius(self, radius):
        print('{0} calledBy {1}'.format(inspect.stack()[0][3],inspect.stack()[1][3]))
        self.__radius = radius
        
    