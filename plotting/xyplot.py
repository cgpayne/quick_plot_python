#!/usr/bin/env python

import os
import sys
import ConfigParser
from matplotlib.pylab import *

filename = sys.argv[1]    # the file containing the data - output will be basename.pdf
confile = sys.argv[2]     # the plotting config file, see 'config.in' for the default structure


def ConfigSectionMap(section):
  dict1 = {}
  options = Config.options(section)
  for option in options:
    try:
      dict1[option] = Config.get(section, option)
      if dict1[option] == -1:
        DebugPrint("skip: %s" % option)
    except:
      print("exception on %s!" % option)
      dict1[option] = None
  return dict1

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


# set-up the config
Config = ConfigParser.ConfigParser()
Config.optionxform=str  # this overrides the default case-insensitivity
Config.read(confile)
klabs = ConfigSectionMap('klabs')
xylims = ConfigSectionMap('xylims')
figparms = ConfigSectionMap('figparms')
klines = ConfigSectionMap('klines')
kcolors = ConfigSectionMap('kcolors')

# do some prep
filebase, fileext = os.path.splitext(filename)
filebase = os.path.basename(filebase)
data = ParseFile(filename)
fig = figure(figsize=(float(figparms['Xlen']),float(figparms['Ylen'])))

# plot the stuff
plotopt = figparms['opt']
for kind in sorted(data):
  if plotopt == 'a':
    plot(data[kind]['x'], data[kind]['y'], klines[str(kind)], color=kcolors[str(kind)], label=klabs[str(kind)])
  elif plotopt == 'b':
    semilogy(data[kind]['x'], data[kind]['y'], klines[str(kind)], color=kcolors[str(kind)], label=klabs[str(kind)])
  elif plotopt == 'c':
    loglog(data[kind]['x'], data[kind]['y'], klines[str(kind)], color=kcolors[str(kind)], label=klabs[str(kind)])
  else:
    print 'figparms[opt] not recognized!'
    print 'figparms[opt] =',plotopt
    print 'exiting...'
    exit()

# set the limits
if xylims['xyauto'] == 'on':
  xdel = float(xylims['xdel'])
  ydel = float(xylims['ydel'])
  xlim(hmin(data,'x')-xdel, hmax(data,'x')+xdel)
  ylim(hmin(data,'y')-ydel, hmax(data,'y')+ydel)
else:
  xlim(float(xylims['xmin']), float(xylims['xmax']))
  ylim(float(xylims['ymin']), float(xylims['ymax']))

# other formatting
legend(loc=figparms['legpos'], fancybox=0, edgecolor='black')
tick_params(which='both', direction='in', left=1, bottom=1, top=1, right=1)
tight_layout()


savefig(filebase + '_plot' + '.pdf')
show()

