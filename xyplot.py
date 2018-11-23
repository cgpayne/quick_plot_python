#!/usr/bin/env python

import sys
from matplotlib.pylab import *


filebase = sys.argv[1]
curvenum = int(sys.argv[2])
strlab = sys.argv[3:3+curvenum]

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


data = ParseFile(filebase + '.dat')
kcolor = {0:'blue', 1:'red', 2:'green', 3:'orange', 4:'purple', 5:'yellow'}
klines = {0:'-', 1:'-', 2:'-o', 3:'-o', 4:'-o', 5:'-o'}
fig = figure(figsize=(6,6))


for kind in sorted(data):
  #plot(data[kind]['x'], data[kind]['y'], klines[kind], color=kcolor[kind], label=datlab[kind])
  semilogy(data[kind]['x'], data[kind]['y'], klines[kind], color=kcolor[kind], label=datlab[kind])

xdel=0
ydel=0
#xlim(hmin(data,'x')-xdel, hmax(data,'x')+xdel)
#ylim(hmin(data,'y')-ydel, hmax(data,'y')+ydel)
xlim(0, 3)
ylim(0.00005, 1)

legend(loc='lower left')


plt.tight_layout()
savefig(filebase + '_plot' + '.pdf')

show()

