# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/
# python.exe -m doctest  stackFrame.py # stackFrame.py is argv to doctest.script
# from __future__ import print_function


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __setattr__(self, name, value):# __init__ will call __setattr__
        if not name in self.__dict__:
            self.__dict__[name] = value
        elif name == 'x' or name == 'y':
            raise TypeError('Point(x, y) is immutable')
        else:
            self.__dict__[name] = value    
    
    def __eq__(self, that):
        if not isinstance(that, Point):
            return False
        return self.x == that.x and self.y == that.y
        
    def __hash__(self):
        return 41 * (41 + self.x) + self.y
        
    def __getattr__(self, name):
      s = 'no def: ' + name + ' arity: %d'
      return lambda *a: print(s % len(a))        

p1 = Point(1, 1)
p2 = Point(1, 1)
p1 == p2
pset = {p1}
print(p1 in pset)
#p1.x = 2 
p1.z(1,3,7)


