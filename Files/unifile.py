# abcdefgh穿山甲到?
s=b'\xe7\xa9\xbf\xe5\xb1\xb1\xe7\x94\xb2\xe5\x88\xb0\xe7\xa9\xbf\xe5\xb1\xb1\xe7\x94\xb2\xe5\x88\xb0\xe5\xba\x95\xe8\xaf\xb4\xe4\xba\x86\xe4\xbb\x80\xe4\xb9\x88\xef\xbc\x9f'
#当你上行那么写时，'\xe7'是四个ascii字符，写入py源码文件中。而本文第一行的四个中文是二进制 'e7'写入py文件
#当python解释器读到s=b''这个写法时，它解释器负责把\xe7这四个字符，理解为二进制的e7
#因为\x是有意义的
sd = s.decode('utf-8') 
print(sd)
print()
with open('chinese.txt','wb') as fb:
    fb.write(s)#我用二进制方式写进文件，那么以UFT8打开就可以正确显示

with open('chinese.txt','r',encoding='latin-1') as fb:#文件的读写操作默认使用系统编码，可以通过调用 sys.getdefaultencoding() 来得到
    st1= fb.read()#read会失败，以OS默认的gbk去解码(decode)会失败 也即是'cp936'
    #http://www.crifan.com/summary_python_unicodedecode_error_possible_reasons_and_solutions/
    #encoding='cp936' 'gbk'
    pass
'''
latin-1 encoding is notable in that it will never produce
a decoding error when reading text of a possibly unknown encoding. Reading a file as
latin-1 might not produce a completely correct text decoding, but it still might be
enough to extract useful data out of it. Also, if you later write the data back out, the
original input data will be preserved.
'''    


with open('chinese.txt','r',encoding='utf-8',errors='replace') as fb:
    st2= fb.read()#read会成功，因为我指定了解码格式是utf-8   
    #如果你在控制台print st那个东东，那个unicode的st又会被编码(encode)为gbk去给微软console
    
s='\xe7\xa9\xbf\xe5\xb1\xb1\xe7\x94\xb2\xe5\x88\xb0\xe5\xba\x95\xe8\xaf\xb4\xe4\xba\x86\xe4\xbb\x80\xe4\xb9\x88\xef\xbc\x9f' 
s.encode(encoding='latin-1',errors='replace').decode('utf-8') 
#这里，因为s是str的字面量，所以没有decode方法。只有byte才有decode方法。
#The default encoding is "utf-8". Many encodings are supported
b='A\xE4B'.encode('latin-1')# 
d=str(b'A\xE4B','latin-1')#The str() built-in function allows you to specify an encoding that will be used to decode 8-bit data as Unicode.
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
    
#next is decoding binary from base64
import base64
code=b'''
MBAPACTIVATE#fDNZSudA5BS47HekIpcs0IKF9Ut4MnreDiIF8KeEtcM=
'''    
binary = base64.b64decode(code)
print(binary)
with open('bin.dat','wb') as fb:
    fb.write(binary)