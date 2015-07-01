#python -c "
from __future__ import print_function; 
import re;import sys;
datepat=re.compile(r'(\d+)[/-]?(\d+)[/-]?(\d+)\D'
                    r'([01][0-9]):([0-5][0-9])');
[print(datepat.sub(r'\2/\3/\1T\4:\5',ln) if datepat.search(ln) else '' )for ln in sys.stdin if ' ' in ln ]
#python pythonRegTemplate.py < log.txt
