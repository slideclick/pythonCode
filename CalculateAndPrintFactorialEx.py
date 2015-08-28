NULL = None 
def CalculateAndPrintFactorialEx(dwNumber,  
                                 hOutputDevice,  
                                 lpLparam,  
                                 lpWparam,  
                                 lpsscSecurity,  
                                 *dwReserved):  
    if lpsscSecurity != NULL:  
        return NULL #Not implemented  
    dwResult = dwCounter = 1 
    while dwCounter <= dwNumber:  
        dwResult *= dwCounter  
        dwCounter += 1 
    hOutputDevice.write(str(dwResult))  
    hOutputDevice.write('\n')  
    return dwResult 
import sys  
CalculateAndPrintFactorialEx(6, sys.stdout, NULL, NULL, NULL,  
 NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL) 
 
def new(cls, *args, **kwargs):  
    return cls(*args, **kwargs)  
   
class Number(object):  
    pass 
   
class IntegralNumber(int, Number):  
    def toInt(self):  
        return new (int, self)  
   
class InternalBase(object):  
    def __init__(self, base):  
        self.base = base.toInt()  
   
    def getBase(self):  
        return new (IntegralNumber, self.base)  
   
class MathematicsSystem(object):  
    def __init__(self, ibase):  
        Abstract  
   
    @classmethod 
    def getInstance(cls, ibase):  
        try:  
            cls.__instance  
        except AttributeError:  
            cls.__instance = new (cls, ibase)  
        return cls.__instance  
   
class StandardMathematicsSystem(MathematicsSystem):  
    def __init__(self, ibase):  
        if ibase.getBase() != new (IntegralNumber, 2):  
            raise NotImplementedError  
        self.base = ibase.getBase()  
   
    def calculateFactorial(self, target):  
        result = new (IntegralNumber, 1)  
        i = new (IntegralNumber, 2)  
        while i <= target:  
            result = result * i  
            i = i + new (IntegralNumber, 1)  
        return result  
   
print StandardMathematicsSystem.getInstance(new (InternalBase,  
new (IntegralNumber, 2))).calculateFactorial(new (IntegralNumber, 6)) 