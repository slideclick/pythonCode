# -*- coding: UTF-8 -*-
# http://www.pythontutor.com/
# python.exe -m doctest  stackFrame.py # stackFrame.py is argv to doctest.script
# from __future__ import print_function
import argparse

import re
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
        #log('{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result))
        log('-> {0}'.format(result,))
        return result
    return wrapped
    
def log(message):
    """Print an indented message (used with trace)."""
    if type(message) is not str:
        message = str(message)
    print(PREFIX + re.sub('\n', '\n' + PREFIX, message))

isa = isinstance
    
def tokenize(s):
    '''
    "Convert a string into a list of tokens."
    
    >>> tokenize('(+(* 3 4)5)') #必须有空格在>>> 后面 下面必须严格对齐第一个>
    ['(', '+', '(', '*', '3', '4', ')', '5', ')']
    '''
    return s.replace('(',' ( ').replace(')',' ) ').split()

def atom(token):
	"Numbers become numbers; every other token is a symbol."
	try: return Number(int(token))
	except ValueError:
		try: return float(token)
		except ValueError:
			if '/' in token:
				num,deno = token.split('/')
				return Fraction(num,deno)
			elif 'i' in token and '+' in token:
##				temp = eval(token.replace('i', 'j', 1))#try: return complex(token.replace('i', 'j', 1))
				temp = token.replace('i', 'j', 1)
				real,image = token.split('+')
				temp = MComplex(real,image[:-1])
				if isa(temp,MComplex): # isa and type return SAME for primitive type including complex
					return temp
				else:
					return str(token)
			else:
				return (Variable(token)    )
                
def printTreeIndented(tree, level=0):
  if tree == None: return
  printTreeIndented(tree.right, level+1)
  print ('  '*level + str(tree.cargo))
  printTreeIndented(tree.left, level+1)
                
def CreateTree(code):
    print (code.replace('(',' ( ').replace(')',' ) '))
    tokens = tokenize(code)
    print (tokens)
    ast = reCreateTree(tokens)
    #printTreeIndented(ast)
    return  ast
@trace
def reCreateTree(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    result = None
    token = tokens.pop(0)
    if '(' == token:
        op= tokens.pop(0)
        result = Add() if op == '+' else (  Multiply(op) if op == '*' else  \
        LessThan() if op == '<' else \
        If() if op == 'if' else \
        While() if op  == 'while'  else \
        Let() if op == 'let' else \
        Assign() if op == 'assign' else Tree(op))
        
        if isa(result,If):
            result.condition = reCreateTree(tokens)
            result.consequence = reCreateTree(tokens)
            result.alternative = reCreateTree(tokens)
        elif     isa(result,While):
            result.condition = reCreateTree(tokens)
            result.body = reCreateTree(tokens)        
            
        else:
            if '(' == tokens[0]:
                result.left = reCreateTree(tokens)
            else:
                result.left = Tree(atom(tokens.pop(0)))
            if '(' == tokens[0]:
                result.right = reCreateTree(tokens)
            else:
                result.right = Tree(atom(tokens.pop(0)))#记住left is Tree.它被eval()时仅仅返回cargo而不是递归向下
    if ')' != tokens.pop(0)         :
        raise SyntaxError('unexpected )')
    return  result

def GeneraTree(neList):
    result = Tree(neList[0] )
    if isa(neList[1], str) or isa(neList[1], int) or isa(neList[1], MComplex) or isa(neList[1], Fraction):
        result.left = (Tree( neList[1]))
    else:
        result.left= GeneraTree(neList[1])
    if isa(neList[2], str)or isa(neList[2], int) or isa(neList[2], MComplex) or isa(neList[2], Fraction):
        result.right = (Tree( neList[2]))
    else:
        result.right= GeneraTree(neList[2])
    return result    
    
class CommonEqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
        
class Fraction(object):# if no object, type() will return - >   <type 'instance'>, AND type(Fraction) WILL be <type 'classobj'>
# while if there is object, type(Fraction) BE <type 'type'>
    def __init__(self, num, den=1):
        self.num = int(num)
        self.den = int(den)
    def __str__(self):
        return "%d///%d" % (self.num, self.den)

    def __repr__(self):
        return "%d//%d" % (self.num, self.den)
        
    def __mul__(self, object):#很危险，LEGB
        return Fraction(self.num*object.num, self.den*object.den)
    #__rmul__ = __mul__
    def __add__(self, other):
        if type(other) == type(5):
            other = Fraction(other)
        return Fraction(self.num * other.den +\
self.den * other.num,\
self.den * other.den)
    __radd__ = __add__
    
    def __sub__(self,other):
        if isinstance(other,type(5)): #这个other写成object会出错，因为object可以找到LEGB，但是if永远是False
            other = Fraction(other)
        return Fraction(self.num * other.den - self.den * other.num,self.den * other.den)
    
# how to write a logic line in multi phsical lines

# how to use semi comma to with multi ligic line in a phsical line
##a = Fraction(1,3);b = Fraction(1,2);print a + b        


class MComplex(object): #<class '__main__.MComplex'>
	def __init__(self,real,imag=0):
		self.real = float(real)
		self.imag = float(imag)
	def __repr__(self):
		return "MComplex(%s,%s)" % (self.real, self.imag)
	def __str__(self):
		return "(%g+%gi)" % (self.real, self.imag)
	# self + other
	def __add__(self,other):
		return MComplex(self.real + other.real, self.imag + other.imag)
# self - other
	def __sub__(self,other):
		return MComplex(self.real - other.real, self.imag - other.imag)
	#def __mul__(self, object):
	#	raise
        
class Tree(CommonEqualityMixin):
  def __init__(self, cargo, left=None, right=None):
    self.cargo = cargo
    self.left  = left
    self.right = right

  def __str__(self):
    #return '<%s>' % (str(self.cargo),)
    #return '{0}: {1}'.format(self.__class__,str(self.cargo),)
    return  ' ( {0} {1} {2} ) '.format(str(self.cargo)*3,repr(self.left),repr(self.right),) if self.left is not None else str(self.cargo)    
  def __repr__(self):
    return  ' ( {0} {1} {2} ) '.format(str(self.cargo)*2,repr(self.left),repr(self.right),) if self.left is not None else str(self.cargo)
  @trace  
  def eval(self,env):#如果你是Tree(1)它刚好返回python的1这个int东东。但是如果是Boolean就会出错了
        if self.left is not None: raise
        return self.cargo  if   not (  isa(self.cargo, Variable)) else self.cargo.eval(env)#你这就叫调出来的代码。不过比你让Var类派生自tree强多了
    
class Add(Tree):
    """ 加法符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__(left = left,right = right,cargo = '+')
        
    @trace      
    def eval(self,env):
        return Number(self.left.eval(env).value + self.right.eval(env).value)   #Number.new(left.evaluate(environment).value + right.evaluate(environment).value)

        

        
class Let(Tree):
    """ 加法符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__(left = left,right = right,cargo = 'let')
    @trace      
    def eval(self,env):
        if self.left not in env:
            env[self.left] = self.right.eval(env)       
        else: raise         
        
class Assign(Tree):
    """ 加法符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__(left = left,right = right,cargo = 'assign')
        
    @trace      
    def eval(self,env):
        if self.left  in env:
            env[self.left] = self.right.eval(env) 
            return env        
        else: raise  
    
class Machine(object):
    """ 虚拟机
    """
    def __init__(self,  environment):
        self.env = environment
        
    def RunCode(self, code):
        result = code.eval(self.env)
        import pprint;        pprint.pprint(self.env)
        return result
    
class Multiply(Tree):
    """ 乘法符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__('*', left, right)    

class Boolean(CommonEqualityMixin):#对==操作，需要你实现，或者你用value去调用python内置type的
    """ 布尔值符号类型
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'true' if self.value else 'false'

    def __str__(self):
        return str(self.value)
        


class Variable(object):
    """ 变量符号类
    """
    def __init__(self, name):
        self.name = name
    
    @trace
    def eval(self,env):
        return env[self.name]   
        
    def __repr__(self):
        return '#{0}#'.format(self.name,)

    def __str__(self):
        return '!{0}!'.format(self.name,)    

class Number(CommonEqualityMixin):
    """ 数值符号类
    """
    def __init__(self, value):
        self.value = value

    def eval(self,env):
        return self   

    def __repr__(self):
        return '\\{0}\\'.format(self.value,)

    def __str__(self):
        return '/{0}/'.format(self.value,)        
        
class If(object):
    """ IF控制语句的实现
    """
    def __init__(self, condition=None, consequence=None, alternative=None):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative       

    @trace
    def eval(self,env):
        cond = self.condition.eval(env); #print (cond)
        if cond == Boolean(True):
            return self.consequence.eval(env)
        elif cond == Boolean(False):
            return self.alternative.eval(env)
            
    def __repr__(self):
        return '( if {0} {1} {2} )'.format(repr(self.condition),repr(self.consequence),repr(self.alternative),)

    def __str__(self):
        return 'if statement'       
        
class While(object):
    def __init__(self, condition=None, body=None):
        self.condition = condition
        self.body = body

    @trace
    def eval(self,env):
        if self.condition.eval(env).value == Boolean(True).value:
            return self.eval(self.body.eval(env))
        elif self.condition.eval(env).value == Boolean(False).value:
            return 
            
    def __repr__(self):
        return '( while {0} {1}  )'.format(repr(self.condition),repr(self.body),)

    def __str__(self):
        return 'while statement'             
            
            
class LessThan(Tree):
    """ 小于符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__(left = left,right = right,cargo = '<')        
    @trace
    def eval(self,env):
        return Boolean(self.left.eval(env).value < self.right.eval(env).value)#Number.new(left.evaluate(environment).value + right.evaluate(environment).value)
        
@trace
def evalTree(t):
    if t.cargo == '+':
        return evalTree(t.left) + evalTree(t.right)
    elif t.cargo == '*':
        return evalTree(t.left) * evalTree(t.right)
    elif t.cargo == '-':
        return evalTree(t.left) - evalTree(t.right)        
    else:
        return t.cargo
        


## UnitTest
import unittest
global_env = {}
class TestCName(unittest.TestCase):
    def setUp(self):
        # Perform set up actions (if any)
        #print('\nsetUp called')
        self.m=Machine({})
        pass
    def tearDown(self):
        # Perform clean-up actions (if any)
        #print('tearDown', 'called')
        del self.m
        pass
                
    def testLessThanAsCondFalse(self):
        #print('testLessThanAsCondFalse', 'called')
        self.assertEqual(CreateTree(' ( if (< 3  2 ) (+ 1 2 ) (+ 3 4))').eval(global_env), Number(7))
    def testLessThanAsCondTrue(self):
        self.assertEqual(CreateTree(' ( if (< 1  2 ) (+ 1 2 ) (+ 3 4))').eval(global_env), Number(3))
    def testLessThanAsCondTrueV(self):
        self.assertEqual(CreateTree(' ( if (< 1  2 ) (+ a 2 ) (+ 3 4))').eval({'a':Number(3)}), Number(5)  )      
    def testLessThanAsValue(self):#下面可以过，但是true其实没有被测试 < 1  2
        self.assertEqual( CreateTree(' ( if (< 1  2 ) (+ (< 3 2) (< 3 1))(+ 1 2))') .eval(global_env), Number(0)  )#Boolean(False)
    def testLet(self):
        
        self.assertEqual(CreateTree(' ( if (< 1  2 ) (+ 1 2 ) (+ 3 4))').eval(global_env), Number(3))        

    
# python.exe -m doctest  diGuiXiaJian.py     
def _test():
    import doctest
    doctest.testmod()

#####################    
#    CreateTree('(*  5 (+ 1  2 ))')

#CreateTree('  (+ a 2 )') .eval({'a':1})
Machine({}).RunCode(Let('a',Number(3)))
Machine({'a':Number(2)}).RunCode(Assign('a',Number(3)))

m=Machine({'a':Number(2)})
m.RunCode(Assign('a',Number(3)))
m.RunCode(CreateTree(' ( if (< 1  2 ) (+ a 2 ) (+ 3 4))'))


m=Machine({})
#m.RunCode(CreateTree(' (let a 4)  '))
#m.RunCode(CreateTree(' ( if (< 1  2 ) (+ a 2 ) (+ 3 4))'))


m=Machine({'b':Number(0)})
m.RunCode(LessThan(Variable('b'),Number(5)))
m.RunCode(Add(Variable('b'),Number(2)))
m.RunCode(Assign(('b'), Add(Variable('b'),Number(2))))


#############################################
if __name__ == "__main__":
        unittest.main()
#following won't be called        
CreateTree('(*  5 (+ 1  2 ))')
CreateTree('(3  5 (4 1  2 ))')
CreateTree('( +( *  5  1)  2 )')
Tree('+', Tree(1),Tree(2)) == Tree('+', Tree(1),Tree(2))
Tree('*',Tree(5), Tree('+',Tree(1),Tree(2)))
Tree('*', Tree('+',Tree(1),Tree(2)),Tree(5))
CreateTree('(*  5 (+ 1  2 ))') == Tree('*', Tree('+',Tree(1),Tree(2)),Tree(5))

CreateTree('(*  5 (+ 1  2 ))') == Tree('*',Tree(5), Tree('+',Tree(1),Tree(2)))#true
CreateTree('(*  5 (+ 1  2 ))') == Tree('*',Tree(5), Add(Tree(1),Tree(2)))#true
CreateTree('(*  5 (+ 1  2 ))') == Multiply(Tree(5), Add(Tree(1),Tree(2)))#true

CreateTree('( * ( + 7 ( * ( * 4  6) ( + 8 9 ) ) ) 5  )') 
CreateTree('(*  5 (+ 1  2 ))')

evalTree( CreateTree('( * ( + 7 ( * ( * 4  6) ( + 8 9 ) ) ) 5  )')    )
evalTree( CreateTree('(*  5 (+ 1  2 ))')    )
evalTree( Tree('*',Tree(5), Tree('+',Tree(1),Tree(2))) )
evalTree( Multiply(Tree(5), Add(Tree(1),Tree(2))) )

CreateTree(' (* 3  2 )').eval(env)


#下面2个输出是不一样的，因为我没有实现乘法的eval它去调用父类的eval。@trace的输出也不一样，因为入口参数用的repr而->后面是__str__
CreateTree('(* 5 (* 3  2 ))').eval(env)
CreateTree('(+ 7(+ 3  2 ))').eval(env)
CreateTree('(+ 7(+ 6/3  2 ))').eval(env)#外围的+需要radd
CreateTree('(- 18/3  2)').eval(env)
CreateTree('(*  5 (+ 1  2 ))').eval(env) #这个根本就不下降，在入口就没有向下call
CreateTree('(+  5 (* 1  2 ))').eval(env) #看这个有意思，理解递归下降：先完成*.然后递归开始回升，出错
evalTree(CreateTree('(- 18/3  2)')  )  #这个可以求值
CreateTree(' (+ 1  2 )').eval(env)# 如果你不print它，它虽然有值，但是不显示，不out而是被丢弃。除非你在脚本里面print它或者在ipython里面敲入它

LessThan(Tree(1),Tree(2)).eval(env)

LessThan(1,2).eval(env)
LessThan(Tree(1),Tree(2)).eval(env)
If(LessThan(Tree(3),Tree(2)),Add(Tree(1),Tree(2)),Add(Tree(3),Tree(4))) .eval(env)
If(LessThan(Tree(1),Tree(2)),Add(Tree(1),Tree(2)),Add(Tree(3),Tree(4))) .eval(env)
While(LessThan(Tree(1),Tree(2)),Add(Tree(1),Tree(2))).eval(env)
CreateTree(' ( if (< 3  2 ) (+ 1 2 ) (+ 3 4))').eval(env)
CreateTree(' ( if (< 1  2 ) 2 (+ 3 4))').eval(env)#这种不带括号的还不行，无法分词
CreateTree(' (< 3  2 )').eval(env)
CreateTree(' (< 1  2 )').eval(env)
CreateTree(' (while  ( < 1 2 )   ( + 1 2 )  ) ')
#   %run diGuiXiaJian.py
# (*  5 (+ 1  2 ))
# ( +( *  5  1)  2 )
# 5 9 8 + 4 6 * * 7 + *
# ( * ( + 7 ( * ( * 4  6) ( + 8 9 ) ) ) 5  )
#EvalArray(Tree('*', Tree('+',Tree(1),Tree(2)),Tree(5)))
        