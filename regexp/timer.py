# Call this by 'python timer.py [-t count] [-O flags]'
# The default count is 500000 and the default flags are null

import sys
import re
from re import *
import time

def timer (pattern, data, repeat) :
    t = time.clock()
    for i in range(0,repeat) :
        result = pattern.search(data)
    t = (time.clock()-t)*1000.0/repeat
    if result :
        sys.stdout.write("Matched %s\n" % repr(result.expand(r'\g<0>')))
    else :
        sys.stdout.write("No match\n")
    sys.stdout.write('Execute time %.3f milliseconds\n' % t)

repeat = 0
flags = ''
args = sys.argv[1:]
while len(args) >= 2 :
    if args[0] == "-t" and re.match(r'^[1-9]\d*$', args[1]) and repeat == 0 :
        repeat = int(args[1])
    elif args[0] == "-O" and flags == '' :
        try:
            flags = eval(args[1])
        except :
            flags = None
        if type(flags) != type(0) :
            sys.stderr.write("Invalid flags specified\n")
            sys.exit(1)
    else :
        break
    args = args[2:]
if len(args) > 0 :
    sys.stderr.write("python timer.py [-t count] [-O flags]\n")
    sys.exit(1)
if repeat == 0 :
    repeat = 500000
if flags == '' :
    flags = 0

while 1 :
    sys.stdout.write('Re> ')
    sys.stdout.flush()
    pattern = sys.stdin.readline()
    if not pattern :
        sys.exit(0)
    pattern = pattern[0:-1].decode("string escape")
    try :
        t = time.clock()
        pat = re.compile(pattern, flags)
        t = (time.clock()-t)*1000.0
        sys.stdout.write('Compile time %.3f milliseconds\n' % t)
        ok = 1
    except :
        sys.stdout.write('The pattern was rejected\n')
        ok = 0

    while ok :
        sys.stdout.write('Data> ')
        sys.stdout.flush()
        data = sys.stdin.readline()
        if not data :
            sys.exit(0)
        data = data[0:-1].decode("string escape")
        if len(data) == 0 :
            break
        timer(pat, data, repeat)
