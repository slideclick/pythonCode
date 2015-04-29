# -*- coding: UTF-8 -*-

#from __future__ import print_function

import sys

def main(fname='null'):
    with open(fname) as f:

        lines = [l for l in f if 'warning' in l]
        lines3 = [l[l.find('warning ') :] for l in lines if 'warning' in l]
        lines4 = [l.split(':') for l in lines3 ]
        [print(l) for l in lines4]
    pass

if __name__ == '__main__':
    #print(sys.argv[1:])
    main(sys.argv[1])
