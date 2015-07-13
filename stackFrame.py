# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/
# from __future__ import print_function

def foo():
    """ simple funciton to demo LEGB and doctest
    
    foo() won't out put at console.
    To output you need print(foo()) which is 3 or python -i foo() which is '3'(Out)
    Example: (There must be a space char after >>> . The Expected result should be what in iPython: '3' not 3)
    However, if you have output in foo, it will also check the print result. You'd better separate output and return value and use doctest to check return value 
    >>> foo()
    '3'
    """
    x = 1
    def bar(y):
        z = y + 2  # <--- (3) ... and the interpreter is here.
        return z
    print 7
    return str(bar(x))  # <--- (2) ... which is returning a call to bar ...
foo()    

def play(myInt, myLongInt, myList, myString):
    print 'START OF play Function:'
    print '\tmyInt=',myInt,'myLongInt=',myLongInt
    print '\tmyList=',myList,'myString=',myString
    myInt += 1
    myLongInt += 1
    myList.append(1)
    myString +='a'
    print 'END OF play Function:'
    print '\tmyInt=',myInt,'myLongInt=',myLongInt
    print '\tmyList=',myList,'myString=',myString
    return
    
    
anInt = 10
aLongInt = 123456789012345678901234567890L
aList = range(5)
aString = 'hello'

print 'BEFORE CALL:'
print 'anInt=',anInt,'aLongInt=',aLongInt
print 'aList=',aList,'aString=',aString
print
play(anInt, aLongInt, aList, aString)
print
print 'AFTER CALL:'
print 'anInt=',anInt,'aLongInt=',aLongInt
print 'aList=',aList,'aString=',aString    




if __name__ == '__main__':
    import doctest
    doctest.testmod()