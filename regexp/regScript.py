# -*- coding: UTF-8 -*-
#python -c "
from __future__ import print_function; 
import re;import sys;
datepat=re.compile(r'(\d+)[/-]?(\d+)[/-]?(\d+)\D'
                    r'([01][0-9]):([0-5][0-9])');
[print(datepat.sub(r'\2/\3/\1T\4:\5',ln) \
if datepat.search(ln) else None )\
for ln in sys.stdin.readlines() \
if ' ' in ln ]
#python regScript.py < log.txt
#2013-03-29 19:13:25:848 Info 2 960  
#2013-04-01 15:58:53:432 Info 2 3864
