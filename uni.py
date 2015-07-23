# -*- coding: UTF-8 -*-
from __future__ import print_function
import inspect
import sys
import pprint
import functools
import argparse
import re
m=re.search(ur'^[发]+$',u'发发发')#前面代码p2工作良好。但是去掉第一个u ，p3可以才能编译 此时p2能编译但是找不到
if m:
    print (m.group(),m.start(),m.end())