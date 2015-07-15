# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/ http://openhome.cc/Gossip/Python/Descriptor.html
# python.exe -m doctest  stackFrame.py # stackFrame.py is argv to doctest.script
# from __future__ import print_function

import inspect

def prop(getter, setter, deleter):
    class PropDesc:
        def __get__(self, instance, owner):
            return getter(instance)
        def __set__(self, instance, value):
            setter(instance, value)
        def __delete__(self, instance):
            deleter(instance)
            
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