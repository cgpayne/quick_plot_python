#!/usr/bin/env python

import sys
import numpy as np


infile = sys.argv[1]
outfile = sys.argv[2]
colm = int(sys.argv[3])
opt = int(sys.argv[4])  # see the if-else ladder below


matrix = open(infile).read()
matrix = [item.split() for item in matrix.split('\n')[:-1]]
matrix = np.array(matrix)
A = matrix[:,[0,colm]]

with open(outfile,'wb') as f:
  for i in range(0,A.shape[0]):
    if opt == 0:
      line = str(A[i,0]) + '\t' + str(A[i,1]) + '\n'
    elif opt == 1:
      line = str(A[i,0]) + '\t' + str(abs(float(A[i,1]))) + '\n'
    else:
      print 'opt not recognized!'
      print 'opt = ', opt
      print 'exiting...'
      exit()
    f.write(line) 

f.close()
