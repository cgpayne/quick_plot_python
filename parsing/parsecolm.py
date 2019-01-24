#!/usr/bin/env python

import sys
import numpy as np


infile = sys.argv[1]       # input file name
outfile = sys.argv[2]      # output file name
popt = sys.argv[3]         # 'a' = (data), 'b' = abs(data)
colm = int(sys.argv[4])    # number of the column (start counting at 0) which you want to parse out


matrix = open(infile).read()
matrix = [item.split() for item in matrix.split('\n')[:-1]]
matrix = np.array(matrix)
A = matrix[:,[0,colm]]

with open(outfile,'wb') as f:
  for i in range(0,A.shape[0]):
    if popt == 'a':
      line = str(A[i,0]) + '\t' + str(A[i,1]) + '\n'
    elif popt == 'b':
      line = str(A[i,0]) + '\t' + str(abs(float(A[i,1]))) + '\n'
    else:
      print 'popt not recognized!'
      print 'popt = ', popt
      print 'exiting...'
      exit()
    f.write(line)

f.close()
