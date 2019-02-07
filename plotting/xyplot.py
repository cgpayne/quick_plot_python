#!/usr/bin/env python

import os
import sys
from matplotlib.pylab import *

filename = sys.argv[1]             # the file containing the data - output will be basename.pdf
plotopt = sys.argv[2]              # 'a' = plot, 'b' = semilogy
curvenum = int(sys.argv[3])        # the number of curves to be plotted (on the same single basic plot)
strlab = sys.argv[4:4+curvenum]    # the subsequent curve labels, for eg: 'exp' 'GH' '$\hbar\tilde{\omega}=10$' '$\hbar\tilde{\omega}=13$' '$\hbar\tilde{\omega}=15$' '$\hbar\tilde{\omega}=20$'

klines = {0:'-', 1:'-', 2:'-', 3:'-', 4:'-', 5:'-'}
#klines = {0:'-o', 1:'-o', 2:'-o', 3:'-o', 4:'-o', 5:'-o'}
kcolor = {0:'blue', 1:'red', 2:'green', 3:'orange', 4:'purple', 5:'yellow'}
legpos = 'lower right'  # 'upper left', 'upper right', 'lower left', 'lower right'
figXlen = 9
figYlen = 6


#xyauto = 'on'
#xdel = 0
#ydel = 0

xyauto = 'off'
xmin = 5
xmax = 55
ymin = 4e-41
ymax = 4.1e-39


datlab  = {}
for i in range(curvenum):
  datlab[i] = strlab[i]


def ParseFile(fname):
  f = open(fname)
  data = {}
  for line in f:
    if '#' in line: continue
    ldat = line.split()
    kind = int(ldat[0])
    if kind not in data: data[kind] = {'x':[], 'y':[]}
    data[kind]['x'].append( float(ldat[1]) )
    data[kind]['y'].append( float(ldat[2]) )
  return data

def hmin(array, string):
  mins = []
  for i in range(0, len(array)):
    mins.append( min(array[i][string]) )
  return min(mins)

def hmax(array, string):
  maxes = []
  for i in range(0, len(array)):
    maxes.append( max(array[i][string]) )
  return max(maxes)


filebase, fileext = os.path.splitext(filename)
filebase = os.path.basename(filebase)
data = ParseFile(filename)
fig = figure(figsize=(figXlen,figYlen))


for kind in sorted(data):
  if plotopt == 'a':
    plot(data[kind]['x'], data[kind]['y'], klines[kind], color=kcolor[kind], label=datlab[kind])
  elif plotopt == 'b':
    semilogy(data[kind]['x'], data[kind]['y'], klines[kind], color=kcolor[kind], label=datlab[kind])
  else:
    print 'plotopt not recognized!'
    print 'plotopt = ', plotopt
    print 'exiting...'
    exit()

if xyauto == 'on':
  xlim(hmin(data,'x')-xdel, hmax(data,'x')+xdel)
  ylim(hmin(data,'y')-ydel, hmax(data,'y')+ydel)
else:
  xlim(xmin, xmax)
  ylim(ymin, ymax)

legend(loc=legpos)


tight_layout()
savefig(filebase + '_plot' + '.pdf')

show()

