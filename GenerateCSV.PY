# -*- coding: UTF-8 -*-
from __future__ import print_function
__author__ = ''

import sys
import argparse
import itertools
import random
Count = 0
def main():
    name = (list(itertools.product('ABCDEFGHIJKLMNOPQRSTUVWZXYabcdefghigklmnopqrstuvwxyz',repeat=2)))
    #print (random.choice(range(32,42)))
    result = []
    global Count
    for n in name:
        line =  (str(n[0])+str(n[1])+','+str(random.choice(range(32,42)))+','+ str(random.choice([1,2])))
        lines =  line.split(',')
        #print (lines)
        if lines[2] == '1': #这里开始写整数 1 居然不报错，但是根本进不来
            if lines[1] > '38': #这里开始写整数，则一直为True. 看来生成csv的好办法是最后再弄Str，开始都用int比较好
                Count +=1
                if random.choice([0,1,2]) % 2 == 0:
                    lines[1] = random.choice(['37','36','33','32','34','35',])
        strline = ','.join(lines)
        result.append(strline)
        print(strline)
    #print(result)
    print(Count)
    pass

if __name__ == '__main__':
    #print(sys.argv[1:])
    parser = argparse.ArgumentParser(description='This is a PyMOTW sample program')
    main()
