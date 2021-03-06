# -*- coding: UTF-8 -*-
from __future__ import print_function
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
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def atom(token):
	"Numbers become numbers; every other token is a symbol."
	try: return int(token)
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
				return str(token)    
                
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
        If() if op == 'if' else Tree(op))
        
        if isa(result,If):
            result.condition = reCreateTree(tokens)
            result.consequence = reCreateTree(tokens)
            result.alternative = reCreateTree(tokens)
        else:
            if '(' == tokens[0]:
                result.left = reCreateTree(tokens)
            else:
                result.left = Tree(atom(tokens.pop(0)))
            if '(' == tokens[0]:
                result.right = reCreateTree(tokens)
            else:
                result.right = Tree(atom(tokens.pop(0)))
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
  def eval(self):
        return self.cargo      
    
class Add(Tree):
    """ 加法符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__(left = left,right = right,cargo = '+')
    @trace      
    def eval(self):
        return self.left.eval() + self.right.eval()   

class Multiply(Tree):
    """ 乘法符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__('*', left, right)    

class Boolean(object):
    """ 布尔值符号类型
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'true' if self.value else 'false'

    def __str__(self):
        return str(self.value)
        
class If(object):
    """ IF控制语句的实现
    """
    def __init__(self, condition=None, consequence=None, alternative=None):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative       

    def eval(self):
        if self.condition.eval().value == Boolean(True).value:
            return self.consequence.eval()
        elif self.condition.eval().value == Boolean(False).value:
            return self.alternative.eval()
            
    def __repr__(self):
        return '( if {0} {1} {2} )'.format(repr(self.condition),repr(self.consequence),repr(self.alternative),)

    def __str__(self):
        return 'if statement'           

class LessThan(Tree):
    """ 小于符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__(left = left,right = right,cargo = '<')        
    @trace
    def eval(self):
        return Boolean(self.left.eval() < self.right.eval())
        
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

CreateTree(' (* 3  2 )').eval()


#下面2个输出是不一样的，因为我没有实现乘法的eval它去调用父类的eval。@trace的输出也不一样，因为入口参数用的repr而->后面是__str__
CreateTree('(* 5 (* 3  2 ))').eval()
CreateTree('(+ 7(+ 3  2 ))').eval()
CreateTree('(+ 7(+ 6/3  2 ))').eval()#外围的+需要radd
CreateTree('(- 18/3  2)').eval()
CreateTree('(*  5 (+ 1  2 ))').eval() #这个根本就不下降，在入口就没有向下call
CreateTree('(+  5 (* 1  2 ))').eval() #看这个有意思，理解递归下降：先完成*.然后递归开始回升，出错
evalTree(CreateTree('(- 18/3  2)')  )  #这个可以求值
CreateTree(' (+ 1  2 )').eval()# 如果你不print它，它虽然有值，但是不显示，不out而是被丢弃。除非你在脚本里面print它或者在ipython里面敲入它


LessThan(1,2).eval()
LessThan(Tree(1),Tree(2)).eval()
If(LessThan(Tree(3),Tree(2)),Add(Tree(1),Tree(2)),Add(Tree(3),Tree(4))) .eval()
If(LessThan(Tree(1),Tree(2)),Add(Tree(1),Tree(2)),Add(Tree(3),Tree(4))) .eval()
CreateTree(' ( if (< 3  2 ) (+ 1 2 ) (+ 3 4))').eval()
CreateTree(' ( if (< 1  2 ) 2 (+ 3 4))').eval()#这种不带括号的还不行，无法分词
CreateTree(' (< 3  2 )').eval()
CreateTree(' (< 1  2 )').eval()
#   %run diGuiXiaJian.py
# (*  5 (+ 1  2 ))
# ( +( *  5  1)  2 )
# 5 9 8 + 4 6 * * 7 + *
# ( * ( + 7 ( * ( * 4  6) ( + 8 9 ) ) ) 5  )
#EvalArray(Tree('*', Tree('+',Tree(1),Tree(2)),Tree(5)))
    
if __name__ == '__main__':
    pass    