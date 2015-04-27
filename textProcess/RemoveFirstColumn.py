#from __future__ import print_function

with open('./msr_paraphrase_data.txt', 'r') as in_file,\
     open('./sentences.txt', 'w+') as out_file:

    next(in_file)
    for in_line in in_file:
        line = in_line.split('\t')[1]
        print(line, file=out_file)