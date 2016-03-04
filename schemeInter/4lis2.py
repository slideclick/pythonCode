################ Symbol, Env classes
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
            log(fn.__name__ + ' exited via exception')
            _PREFIX = _PREFIX[:-4]
            raise
        # Here, print out the return value.
        print '{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result)
        return result
    return wrapped
    
def primitivePlus (*operands):
    if (len(operands) == 0):
       return 0
    else:
       return operands[0] + primitivePlus (*(operands[1:])) # thus + can support more than 2 argements

 
       
class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if var in self else self.outer.find(var)

def add_globals(env):
    "Add some Scheme standard procedures to an environment."
    import math, operator as op
    env.update(
     {'+':primitivePlus#op.add, # thus + can support more than 2 argements, op.add only support 2 arguments
     ,'-':op.sub,
     '*':int.__mul__,
     '<=':op.le,
     'list':lambda *x:list(x)
})
    return env

global_env = add_globals(Env())
isa = isinstance

class Procedure:
    def __init__(self, params, body, env):
        self._params = params
        self._body = body
        self._env = env
    def getParams(self):
        return self._params
    def getBody(self):
        return self._body
    def getEnvironment(self):
        return self._env        
    def __str__(self):
        return '<Procedure %s / %s>' % (str(self._params), str(self._body))
################ eval
@trace
def meval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isa(x, str):             # variable reference
        return env.find(x)[x]
    elif not isa(x, list):         # constant literal
        return x                
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        return meval((conseq if meval(test, env) else alt), env)
    elif x[0] == 'set!':           # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = meval(exp, env)
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = meval(exp, env)
    elif x[0] == 'lambda':         # (lambda (var*) exp)
        (_, para, body) = x
        return Procedure(para, body, env)
    elif x[0] == 'begin':          # (begin exp*)
        for exp in x[1:]:
            val = meval(exp, env)
        return val
    else:                          # (proc exp*)
        exps = [meval(exp, env) for exp in x]
        return mapply(exps[0], exps[1:])

@trace    
def mapply(proc, operands):
    if isinstance(proc, Procedure):        
        newenv = Env( proc.getParams(),operands, proc.getEnvironment())    
        return meval(proc.getBody(), newenv)     
    else:
        return proc(*operands)            

################ parse, read, and user interaction
def mparse(s):
    "Read a Scheme expression from a string."
    return read_from(tokenize(s))

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
        

        
def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return str(token)



def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    return '('+' '.join(map(to_string, exp))+')' if isa(exp, list) else str(exp)

#program = " (begin (define r 3) (* 3.141592653 (* r r))) "
#mparse(program)
#meval(mparse(program))
'''

(gc ((lambda (x y) (+ y x 1/2)) 4/6 5/3 2)  )

(gc( (lambda (x) (4/6))  1/3)  )

'''
#program = " (gc ((lambda (x y) (+ y x 1/2)) 4/6 5/3 2)  ) "
#program = "    ((lambda (x y) (+ y x 1/2)) 4/6 5/3 2)    "
# mparse(program)
#print meval(mparse(program))
#meval(mparse("     ((lambda (x y) (+ y 2 x )) 4 5)  "))
meval(mparse("    (begin (define myfun(lambda (x y) (+ y 2(- x 1) )))(list 2 3) (myfun 4 5)))  "))
#meval(mparse("    (gc ((lambda (x y) (+ y x 1/2)) 4/6 5/3 2)  )   "))
#meval( " ['gc', [['lambda', ['x', 'y'], ['+', 'y', 'x', <__main__.Fraction instance at 0x02349E68>]], <__main__.Fraction instance at 0x02349A80>, <__main__.Fraction instance at 0x02349FD0>, 2]]    " )


def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = meval(mparse(raw_input(prompt)))
        if val is not None: print to_string(val)
repl()
'''
>>>meval(mparse("    (begin (define myfun(lambda (x y) (+ y 2(- x 1) )))(list 2 3) (myfun 4 5)))  "))
meval(['begin', ['define', 'myfun', ['lambda', ['x', 'y'], ['+', 'y', 2, ['-', 'x', 1]]]], ['list', 2, 3], ['myfun', 4, 5]]):
meval(['define', 'myfun', ['lambda', ['x', 'y'], ['+', 'y', 2, ['-', 'x', 1]]]], {'-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval(['lambda', ['x', 'y'], ['+', 'y', 2, ['-', 'x', 1]]], {'-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval(['lambda', ['x', 'y'], ['+', 'y', 2, ['-', 'x', 1]]], {'-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> <Procedure ['x', 'y'] / ['+', 'y', 2, ['-', 'x', 1]]>
meval(['define', 'myfun', ['lambda', ['x', 'y'], ['+', 'y', 2, ['-', 'x', 1]]]], {'-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> None
meval(['list', 2, 3], {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval('list', {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval('list', {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> <function <lambda> at 0x021CD330>
meval(2, {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval(2, {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> 2
meval(3, {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval(3, {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> 3
mapply(<function <lambda> at 0x021CD330>, [2, 3]):
mapply(<function <lambda> at 0x021CD330>, [2, 3]) -> [2, 3]
meval(['list', 2, 3], {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> [2, 3]
meval(['myfun', 4, 5], {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval('myfun', {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval('myfun', {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> <Procedure ['x', 'y'] / ['+', 'y', 2, ['-', 'x', 1]]>
meval(4, {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval(4, {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> 4
meval(5, {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}):
meval(5, {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> 5
mapply(<__main__.Procedure instance at 0x021D0198>, [4, 5]):
meval(['+', 'y', 2, ['-', 'x', 1]], {'y': 5, 'x': 4}):
meval('+', {'y': 5, 'x': 4}):
meval('+', {'y': 5, 'x': 4}) -> <function primitivePlus at 0x021CD1F0>
meval('y', {'y': 5, 'x': 4}):
meval('y', {'y': 5, 'x': 4}) -> 5
meval(2, {'y': 5, 'x': 4}):
meval(2, {'y': 5, 'x': 4}) -> 2
meval(['-', 'x', 1], {'y': 5, 'x': 4}):
meval('-', {'y': 5, 'x': 4}):
meval('-', {'y': 5, 'x': 4}) -> <built-in function sub>
meval('x', {'y': 5, 'x': 4}):
meval('x', {'y': 5, 'x': 4}) -> 4
meval(1, {'y': 5, 'x': 4}):
meval(1, {'y': 5, 'x': 4}) -> 1
mapply(<built-in function sub>, [4, 1]):
mapply(<built-in function sub>, [4, 1]) -> 3
meval(['-', 'x', 1], {'y': 5, 'x': 4}) -> 3
mapply(<function primitivePlus at 0x021CD1F0>, [5, 2, 3]):
mapply(<function primitivePlus at 0x021CD1F0>, [5, 2, 3]) -> 10
meval(['+', 'y', 2, ['-', 'x', 1]], {'y': 5, 'x': 4}) -> 10
mapply(<__main__.Procedure instance at 0x021D0198>, [4, 5]) -> 10
meval(['myfun', 4, 5], {'myfun': <__main__.Procedure instance at 0x021D0198>, '-': <built-in function sub>, '+': <function primitivePlus at 0x021CD1F0>, 'list': <function <lambda> at 0x021CD330>}) -> 10
meval(['begin', ['define', 'myfun', ['lambda', ['x', 'y'], ['+', 'y', 2, ['-', 'x', 1]]]], ['list', 2, 3], ['myfun', 4, 5]]) -> 10
'''
