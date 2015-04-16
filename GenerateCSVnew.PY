# -*- coding: UTF-8 -*-
from __future__ import print_function
__author__ = ''

import sys
import argparse
import itertools
import random
def main():
    name = (list(itertools.product('ABCDEFGHIJKLMNOPQRSTUVWZXYabcdefghigklmnopqrstuvwxyz',repeat=2)))
    #print (random.choice(range(32,42)))
    for n in name:
        print (str(n[0])+str(n[1])+','+str(random.choice(range(32,42)))+','+ str(random.choice([1,2])))
    pass
if __name__ == '__main__':
    #print(sys.argv[1:])
    parser = argparse.ArgumentParser(description='This is a PyMOTW sample program')
    main()
