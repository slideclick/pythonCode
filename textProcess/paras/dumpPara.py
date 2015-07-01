# -* - coding: UTF-8 -* -


from __future__ import print_function

import collections

paraList=[]
for line in open('paras.txt'):
    #print line
    para = line.split()
    if len(para) > 0:
        paraList.append(para[0])

print (paraList)

arguList=[]
for line in open('argus.txt'):
    arguList=line.split(',')
print (arguList)

map= (zip(paraList,arguList))
#print map
for row_number, k in enumerate(map):
    print (row_number,k)


def main():
    pass
if __name__ == '__main__':
   main()
