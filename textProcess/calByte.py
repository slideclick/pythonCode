import re
pat =  re.compile(r'^.+ (\d{1,}) bytes long.$')
sizeList= []
for ln in open('VSLOG.txt'):
    mat  = pat.search(ln)
    if mat:
        size = mat.group(1)
        sizeList.append(int(size))
print(max(sizeList))
print(len(sizeList))        
print(sum(sizeList))