# -* - coding: UTF-8 -* -

import functools
_PREFIX = ''
def trace(fn):
    """A decorator that prints a function's name, its arguments, and its return
    values each time the function is called. For example,

    @trace
    def compute_something(x, y):
        # function body
    """
    @functools.wraps(fn)
    def wrapped(*args, **kwds):
        global _PREFIX
        reprs = [repr(e) for e in args]
        reprs += [repr(k) + '=' + repr(v) for k, v in kwds.items()]
        print '{0}({1})'.format(fn.__name__, ', '.join(reprs)) + ':'
        _PREFIX += '    '
        try:
            result = fn(*args, **kwds)
            _PREFIX = _PREFIX[:-4]
        except Exception as e:
            print fn.__name__ + ' exited via exception'
            _PREFIX = _PREFIX[:-4]
            raise
        # Here, print out the return value.
        print '{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result)
        return result
    return wrapped


def Plus(*operands):
    if (len(operands) == 0):
       return 0
    else:
       return operands[0] + Plus (*(operands[1:])) # thus + can support more than 2 argements

#@trace
def Bigger(o1, o2):
	if isa(o1,  Fraction):
		#raise
		o1.sth();# duck type
	else:
		return o1 > o2

def Times(o1, o2):
	return o1 * o2


class Fraction(object):# if no object, type() will return - >   <type 'instance'>, AND type(Fraction) WILL be <type 'classobj'>
# while if there is object, type(Fraction) BE <type 'type'>
    def __init__(self, num, den=1):
        self.num = int(num)
        self.den = int(den)
    def __str__(self):
        return "%d/%d" % (self.num, self.den)

    def __mul__(self, object):
        return Fraction(self.num*object.num, self.den*object.den)
    #__rmul__ = __mul__
    def __add__(self, other):
        if type(other) == type(5):
            other = Fraction(other)
        return Fraction(self.num * other.den +\
self.den * other.num,\
self.den * other.den)
    #__radd__ = __add__
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

#这个仅仅支持一般表达式，不支持嵌套，被cal调用。仅仅是改为前缀
def mparse(*tokens):
	ast = list()
	#print tokens[1]
	ast.append( tokens[1])
	ast.append( atom(tokens[0]))
	ast.append( atom(tokens[2]))
	return ast

def checkSyntax(ast):
	if not ast[0]  in operators:
		raise

def staticSemChen(ast):
	#(oper,o1,o1) = ast
	if isa(ast[1],  Fraction) and 		isa(ast[2],  Fraction)  and ast[0] =='>':
		raise
	elif isa(ast[1],  complex) and 		isa(ast[2],  complex)  and ast[0] =='>':
		raise

def cal(expr):
	tokens =  expr.split()# default space
	ast = mparse(*tokens)
	checkSyntax(ast)
	staticSemChen(ast)
	return table[ast[0]](*ast[1:])
	#print tokens;print ast



def test():
	#print cal('1 - 2')
	print cal('1 + 2')
	print cal('1 > 2')
	print cal('1 * 2')
	print cal('3/4 + 1/2')
	print cal('3/4 * 1/2')
	#print cal('3/4 > 1/2')
	print cal('3+4i + 1+2i')
	print cal('3+4i * 1+2i')
	#print cal('3+4i > 1+2i')

	print cal('hello + world')

	print cal('hello > world')

	#print cal('hello * world')
################ parse, read, and user interaction
def mparse2(s):
    "Read a Scheme expression from a string."
    result = None
    result = read_from(tokenize(s))
##    GeneraTree(result)# immuatale
    return result

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)
################ 不用nlist试试用树，走树方式计算
class Tree:
  def __init__(self, cargo, left=None, right=None):
    self.cargo = cargo
    self.left  = left
    self.right = right
  def __str__(self):
    return str(self.cargo)
  def __repr__(self):
    return str(self.cargo)
#把 nlist转换为tree
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

#@trace 走树方式计算
def evalTree(t):
    if t.cargo == '+':
        return evalTree(t.left) + evalTree(t.right)
    elif t.cargo == '*':
        return evalTree(t.left) * evalTree(t.right)
    else:
        return t.cargo

#这个是用字典代替二叉树的孩子，实验表达式求值 走树方式计算
class CTree:
  def __init__(self, cargo):
    self.cargo = cargo
    self.childs={}
  def __str__(self):
    return str(self.cargo)
  def __repr__(self):
    return str(self.cargo)

##@trace
def GeneraCTree(neList):
    result = CTree(neList[0] )
    for i in range(1, len(neList)):
        if isa (neList[i],list):
            result.childs[i] =GeneraCTree(neList[i])
        else:
            result.childs[i] =CTree(neList[i])
    return result

##@trace
def evalCTree(t):
    if t.childs <> {}:#t.cargo in table:
        argu = []
        for i in range(1,  1+ len(list(t.childs))):
            argu.append(t.childs[i])
        for i in range(len(argu)):
            argu[i] = evalCTree(argu[i])#这里用了mutalbe数组，也许递归回来有问题
        return table[t.cargo](*argu)
    else:
        return t.cargo
############################################

#这个是走树时生成虚拟机指令

CodeArry = {}
StackRunTime = {}
sp = 0
pc = 0
@trace
def ADDI():
    global sp
    global pc
    global CodeArry
    global StackRunTime
    sp -=1
    right = StackRunTime[sp]
    sp -=1
    left = StackRunTime[sp]
    StackRunTime[sp] = left + right
    sp +=1

def MULI():
    global sp
    global pc
    global CodeArry
    global StackRunTime
    sp -=1
    right = StackRunTime[sp]
    sp -=1
    left = StackRunTime[sp]
    StackRunTime[sp] = left * right
    sp +=1
@trace
def PUSHI():
    global sp
    global pc
    global CodeArry
    global StackRunTime
    StackRunTime[sp] =CodeArry[pc]
    sp +=1
    pc +=1


def GeneraeArray(t ,codep = 0):
    if t.cargo == '+':
        #return evalTree(t.left) + evalTree(t.right)
        codep =GeneraeArray(t.left,codep)
        codep =GeneraeArray(t.right,codep)
        CodeArry[codep] = ADDI
        codep += 1
        return codep
    elif t.cargo == '*':
##        return evalTree(t.left) * evalTree(t.right)
        codep =GeneraeArray(t.left,codep)
        codep =GeneraeArray(t.right,codep)
        CodeArry[codep] = MULI
        codep += 1
        return codep
    else:
        CodeArry[codep] = PUSHI
        codep +=1
        CodeArry[codep] = t.cargo
        codep +=1
        return codep

def EvalArray(t):
    global sp
    global pc
    global CodeArry
    global StackRunTime
    pc=GeneraeArray(t)
    for i in range(pc):
        print CodeArry[i]
    CodeArry[pc] = None

    sp = 0
    pc = 0

    while (CodeArry[pc] != None):
        temp = pc
        pc +=1
        CodeArry[temp]()
        for i in range(sp):
            print StackRunTime[i]
    return StackRunTime[0]



#缩进打印
def printTreeIndented(tree, level=0):
  if tree == None: return
  if not isa(tree,Tree):
    raise Exception
  printTreeIndented(tree.right, level+1)
  print '     '*level + str(level) + ': '+ str(tree.cargo)
  printTreeIndented(tree.left, level+1)

#A comma at the end of a print statement prevents a newline from being written...
#这个是用字典模拟树的前向打印
def DprintTreeiOrder(tree):
  if tree == None: return
  if not isa(tree,dict):
    raise Exception
  DprintTreeiOrder(tree[1])
  print tree[0],
  DprintTreeiOrder(tree[2])

#一般树的打印
def printTreePreOrder(tree):
  if tree == None: return
  print tree.cargo,
  printTreePreOrder(tree.left)
  printTreePreOrder(tree.right)

def printTreeInorder(tree):
  if tree == None: return
  printTreeInorder(tree.left)
  print tree.cargo,
  printTreeInorder(tree.right)

def printTreePostorder(tree):
  if tree == None: return
  printTreePostorder(tree.left)
  printTreePostorder(tree.right)
  print tree.cargo,

################ parse, read, and user interaction

#二叉查找树
##indata = [18, 16, 80, 42, 100, 2, 53]
indata = [ 50, 25, 80, 32, 81, 12, 63]
##indata = [12, 25 ,32, 50 ,63 ,80, 81]

def GenerateBtree(indata):
##    global indata
    root = Tree(indata[0])
    for i in range(1,len(indata)):
        InsertBtree(root,Tree(indata[i]))
    return root

def InsertBtree(root, newData):
    if root == None:
        return newData
    if newData.cargo > root.cargo:
        root.right = InsertBtree(root.right,newData)
    else:
        root.left = InsertBtree(root.left,newData)
    return root

#这个是用字典模拟树
def GenerateDDtree(indata):
    CARGO = 0
    root = {1:None,2:None}
    root[CARGO] = indata[CARGO]
    for i in range(1,len(indata)):
        InsertDDtree(root,indata[i])
    return root

def InsertDDtree(root, newData):
    CARGO = 0
    node = {1:None,2:None}
    node[CARGO] = newData
    if root == None:
        return node
    if newData > root[CARGO]:
        root[2] = InsertDDtree(root[2],node)
    else:
        root[1] = InsertDDtree(root[1],node)
    return root


#这个是用数组模拟树
def GenerateDtree(indata):
##    global indata
    root = [None,None,None]
    root[0] = indata[0]
    for i in range(1,len(indata)):
        InsertDtree(root,indata[i])
    return root
@trace
def InsertDtree(root, newData):
    node = [None,None,None]
    node[0] = newData
    if root == None:
        return node
    if newData > root[0]:
        root[2] = InsertDtree(root[2],node)
    else:
        root[1] = InsertDtree(root[1],node)
    return root






def repl(prompt='lis.py> '):
    "A prompt-mparse-meval-print loop."
    global indata
    while True:
        import sys
        code =  sys.stdin.readline()
##        print code
        ast =mparse2(code) #生成nlist
        print ast
        tree =GeneraTree( ast)#二叉树
        ctree =GeneraCTree( ast)#用字典表示childs
##        printTreePostorder(tree )
##        print '\r\n'
##        printTreeInorder(tree)
##        print '\r\n'
##        printTreePreOrder(tree )
##        print '\r\n'
        printTreeIndented(tree)#打印缩进树
        print evalTree(tree)#求值树
        print evalCTree(ctree)#求值树 用字典表示childs
        print EvalArray(tree) #求值虚拟机指令
        printTreeInorder(GenerateBtree(indata))#打印二叉排序树，树的内容前序打印
        printTreeIndented(GenerateBtree(indata))#打印二叉排序树，树的内容缩进打印
        print GenerateDDtree(indata) #用字典代替class 打印出 '树'
        print DprintTreeiOrder(GenerateDDtree(indata)) #用字典代替class 树的内容前序打印
##        print GenerateDtree(indata)


isa = isinstance
operators = ('+','*','>')
caltors =(Plus,Times,Bigger)
table=dict()
table.update(zip(operators,caltors))

if __name__ == '__main__':
    #test()
    repl()
