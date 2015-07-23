# -*- coding: UTF-8 -*-
from __future__ import print_function
import re

# common variables

rawstr = r'(?P<pr>(穿)?)(?P<na>(山甲)+?)(?P<sed>到)\w+(?P=sed)(?(pr)(?P=pr))\w(?P<nam>(a)?)\d\d\d(?(nam)(?P=nam))'
embedded_rawstr = r'(?u)(?P<pr>(穿)?)(?P<na>(山甲)+?)(?P<sed>到)\w+(?P=sed)(?(pr)(?P=pr))\w(?P<nam>(a)?)\d\d\d(?(nam)(?P=nam))'
matchstr = u"""zouzou穿山甲山甲到山甲sa撒到穿要a828accc"""

# method 1: using a compile object
compile_obj = re.compile(rawstr,  re.UNICODE)
match_obj = compile_obj.search(matchstr)

# method 2: using search function (w/ external flags)
match_obj = re.search(rawstr, matchstr,  re.UNICODE)

# method 3: using search function (w/ embedded flags)
match_obj = re.search(embedded_rawstr, matchstr)

# Retrieve group(s) from match_obj
all_groups = match_obj.groups()
print(all_groups)

# Retrieve group(s) by index
group_1 = match_obj.group(1)
group_2 = match_obj.group(2)
group_3 = match_obj.group(3)
group_4 = match_obj.group(4)
group_5 = match_obj.group(5)
group_6 = match_obj.group(6)
group_7 = match_obj.group(7)

# Retrieve group(s) by name
pr = match_obj.group('pr')
na = match_obj.group('na')
sed = match_obj.group('sed')
nam = match_obj.group('nam')

