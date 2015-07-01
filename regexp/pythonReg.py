#python -c "
from __future__ import print_function; 
import re;
datepat=re.compile(r'(\d+)[/-]?(\d+)[/-]?(\d+)\D([01][0-9]):([0-5][0-9])');
[print(datepat.sub(r'\2/\3/\1T\4:\5',ln) if datepat.search(ln) else '' )for ln in open('log.txt') if ' ' in ln ]
[print(datepat.search(ln).group(0,1,2,3,4,5) if datepat.search(ln) else '' )for ln in open('log.txt') if ' ' in ln ]
#"