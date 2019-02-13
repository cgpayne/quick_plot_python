#!/usr/bin/env python

import sys
import numpy as np

infile = sys.argv[1]               # input file name
outfile = sys.argv[2]              # output file name, NOTE: date should correspond to date of infile, whereas dates in data_final correspond to compilation date
popt = sys.argv[3]                 # 'a' = (colmR), 'b' = abs(colmR)
colmL = int(sys.argv[4])           # the column number (start counting at 0) in the data which you would like to be the left column in the output
colmR = int(sys.argv[5])           # " " " " " " " " " " " " " " " " " " right " " " "
scaleL = float(sys.argv[6]) \
  if len(sys.argv) > 6 else 1.0    # scale factor for the left data, set the default value to 1.0
scaleR = float(sys.argv[7]) \
  if len(sys.argv) > 7 else 1.0    # " " " " right ", " " " " " "


# read in and parse the data
matrix = []
with open(infile) as f:
  for line in f:
    if '#' in line: continue
    matrix.append(line.split())
matrix = np.array(matrix)
matrix = matrix[:,[colmL,colmR]]
A = np.zeros(matrix.shape)
for i in range(0,A.shape[0]):
  A[i,0] = float(matrix[i,0])
  A[i,1] = float(matrix[i,1])

# print data to file
with open(outfile,'wb') as f:
  for i in range(0,A.shape[0]):
    if popt == 'a':
      line = str(scaleL*A[i,0]) + '\t' + str(scaleR*A[i,1]) + '\n'
    elif popt == 'b':
      line = str(scaleL*A[i,0]) + '\t' + str(abs(scaleR*A[i,1])) + '\n'
    else:
      print 'popt not recognized!'
      print 'popt = ', popt
      print 'exiting...'
      exit()
    f.write(line)
f.close()

