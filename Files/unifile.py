# abcdefgh穿山甲到?
s=b'\xe7\xa9\xbf\xe5\xb1\xb1\xe7\x94\xb2\xe5\x88\xb0\xe7\xa9\xbf\xe5\xb1\xb1\xe7\x94\xb2\xe5\x88\xb0\xe5\xba\x95\xe8\xaf\xb4\xe4\xba\x86\xe4\xbb\x80\xe4\xb9\x88\xef\xbc\x9f'
#当你上行那么写时，'\xe7'是四个ascii字符，写入py源码文件中。而本文第一行的四个中文是二进制 'e7'写入py文件
#当python解释器读到s=b''这个写法时，它解释器负责把\xe7这四个字符，理解为二进制的e7
sd = s.decode('utf-8') 
print(sd)
print()
with open('chinese.txt','wb') as fb:
    fb.write(s)#我用二进制方式写进文件，那么以UFT8打开就可以正确显示

with open('chinese.txt','r') as fb:
    #st= fb.read()#read会失败，以OS默认的gbk去解码(decode)会失败 也即是'cp936'
    #http://www.crifan.com/summary_python_unicodedecode_error_possible_reasons_and_solutions/
    #encoding='cp936' 'gbk'
    pass
with open('chinese.txt','r',encoding='utf-8',errors='replace') as fb:
    st= fb.read()#read会成功，因为我指定了解码格式是utf-8   
    #如果你在控制台print st那个东东，那个unicode的st又会被编码(encode)为gbk去给微软console
    
s='\xe7\xa9\xbf\xe5\xb1\xb1\xe7\x94\xb2\xe5\x88\xb0\xe5\xba\x95\xe8\xaf\xb4\xe4\xba\x86\xe4\xbb\x80\xe4\xb9\x88\xef\xbc\x9f' 
s.encode('latin-1','replace').decode('utf-8') 
 
import re
rs = re.search(r'(a)\w+\1',"cabad") 
if rs:
    print(rs.group())
    print(rs.group(1))
print()    
rs = re.search(r'(山)(.*)\1',sd) 
if rs:
    print(rs.group())
    print(rs.group(0))
    print(rs.group(1))
    print(rs.group(2))
    print(rs.groups())
    print(rs.groupdict())
print()   
rs = re.search(r'(?P<shang>山)(.*)(?P=shang)',sd) 
if rs:
    print(rs.group())
    print(rs.group(0))
    print(rs.group(1))
    print(rs.group(2))

    print(rs.groups())
    print(rs.groupdict())    
    