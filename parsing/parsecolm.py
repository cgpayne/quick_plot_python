#!/usr/bin/env python

import sys
import numpy as np

infile = sys.argv[1]       # input file name
outfile = sys.argv[2]      # output file name
popt = sys.argv[3]         # 'a' = (colmR), 'b' = abs(colmR)
colmL = int(sys.argv[4])   # the column number (start counting at 0) in the data which you would like to be the left column in the output 
colmR = int(sys.argv[5])   # " " " " " " " " " " " " " " " " " " right " " " "


# read in and parse the data
matrix = []
with open(infile) as f:
  for line in f:
    if '#' in line: continue
    matrix.append(line.split())
matrix = np.array(matrix)
A = matrix[:,[colmL,colmR]]

# print data to file
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

