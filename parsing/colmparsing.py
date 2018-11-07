#!/usr/bin/env python

import numpy as np


thefile = '[insert]'
colm = ?


matrix = open(thefile).read()
matrix = [item.split() for item in matrix.split('\n')[:-1]]
matrix = np.array(matrix)
A = matrix[:,[0,colm]]

with open('colmparsing.out','wb') as f:
  for i in range(0,A.shape[0]):
    line = str(A[i,0]) + '\t' + str(A[i,1]) + '\n'
    #line = str(A[i,0]) + '\t' + str(abs(float(A[i,1]))) + '\n'
    f.write(line) 

f.close()
