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
        log('{0}'.format(result,))
        return result
    return wrapped
    
def log(message):
    """Print an indented message (used with trace)."""
    if type(message) is not str:
        message = str(message)
    print(PREFIX + re.sub('\n', '\n' + PREFIX, message))

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
    printTreeIndented(ast)
    return  ast

def reCreateTree(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    result = None
    token = tokens.pop(0)
    if '(' == token:
        op= tokens.pop(0)
        result = Add(op) if op == '+' else (  Multiply(op) if op == '*' else  Tree(op))
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

    
class CommonEqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
        
class Tree(CommonEqualityMixin):
  def __init__(self, cargo, left=None, right=None):
    self.cargo = cargo
    self.left  = left
    self.right = right

  def __str__(self):
    return '{0}: {1}'.format(self.__class__,str(self.cargo),)
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
    """ 加法符号类
    """
    def __init__(self, left=None, right=None):
        super().__init__('*', left, right)        

def evalTree(t):
    if t.cargo == '+':
        return evalTree(t.left) + evalTree(t.right)
    elif t.cargo == '*':
        return evalTree(t.left) * evalTree(t.right)
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
evalTree( CreateTree('( * ( + 7 ( * ( * 4  6) ( + 8 9 ) ) ) 5  )')    )
evalTree( Tree('*',Tree(5), Tree('+',Tree(1),Tree(2))) )
evalTree( Multiply(Tree(5), Add(Tree(1),Tree(2))) )
CreateTree(' (* 3  2 )').eval()
CreateTree('(* 5 (* 3  2 ))').eval()
CreateTree('(+ 7(+ 3  2 ))').eval()
CreateTree(' (+ 1  2 )').eval()# 如果你不print它，它虽然有值，但是不显示，不out而是被丢弃。除非你在脚本里面print它或者在ipython里面敲入它
#   %run diGuiXiaJian.py
# (*  5 (+ 1  2 ))
# ( +( *  5  1)  2 )
# 5 9 8 + 4 6 * * 7 + *
# ( * ( + 7 ( * ( * 4  6) ( + 8 9 ) ) ) 5  )
#EvalArray(Tree('*', Tree('+',Tree(1),Tree(2)),Tree(5)))
    
if __name__ == '__main__':
    pass    