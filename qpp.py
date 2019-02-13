#!/usr/bin/env python

import sys
import ConfigParser
from matplotlib.pylab import *

confile = sys.argv[1]     # the plotting config file, see 'config.in' for the default structure
filename = sys.argv[2]    # pdf output file name (including desired extension)


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

def ParseFile(fname, colmL, colmR, scaleL, scaleR, optL, optR):
  tmpmat = []
  with open(fname) as f:
    for line in f:
      if '#' in line: continue
      tmpmat.append(line.split())
  tmpmat = np.array(tmpmat)
  tmpmat = tmpmat[:,[colmL,colmR]]
  data = np.zeros(tmpmat.shape)
  for i in range(data.shape[0]):
    if optL == 'a':
      data[i,0] = scaleL*float(tmpmat[i,0])
    elif optL == 'b':
      data[i,0] = abs(scaleL*float(tmpmat[i,0]))
    else:
      print 'optL not recognized!'
      print 'fname =',fname
      print 'optL =',optL
      print 'exiting...'
      exit()
    if optR == 'a':
      data[i,1] = scaleR*float(tmpmat[i,1])
    elif optR == 'b':
      data[i,1] = abs(scaleR*float(tmpmat[i,1]))
    else:
      print 'optR not recognized!'
      print 'fname =',fname
      print 'optR =',optR
      print 'exiting...'
      exit()
  return data

def hmin(array, string):
  mins = []
  for i in range(len(array)):
    mins.append(min(array[i][string]))
  return min(mins)

def hmax(array, string):
  maxes = []
  for i in range(len(array)):
    maxes.append(max(array[i][string]))
  return max(maxes)


# set-up the config
Config = ConfigParser.ConfigParser()
Config.optionxform=str  # this overrides the default case-insensitivity
Config.read(confile)
tmp = ConfigSectionMap('tmp')
kfiles = ConfigSectionMap('kfiles')
kcolms = ConfigSectionMap('kcolms')
kscales = ConfigSectionMap('kscales')
kopts = ConfigSectionMap('kopts')
klabs = ConfigSectionMap('klabs')
xylims = ConfigSectionMap('xylims')
figparms = ConfigSectionMap('figparms')
figopts = ConfigSectionMap('figopts')
FS = ConfigSectionMap('FS')
klines = ConfigSectionMap('klines')
kcolors = ConfigSectionMap('kcolors')
korders = ConfigSectionMap('korders')

# some pre-formatting
if figopts['tex'] == 'on':
  matplotlib.rcParams['mathtext.fontset'] = 'stix'    # this is to switch to latex font style
  matplotlib.rcParams['font.family'] = 'STIXGeneral'  # " " " " " " " "

# parse the files for the data
knum = int(tmp['knum'])
data = np.zeros((0,2))
lens = np.zeros(knum, dtype=np.int)
for k in range(knum):
  kL = str(k) + 'L'
  kR = str(k) + 'R'
  tmpdat = ParseFile(kfiles[str(k)], int(kcolms[kL]), int(kcolms[kR]), float(kscales[kL]), float(kscales[kR]), kopts[kL], kopts[kR])
  lens[k] = np.shape(tmpdat)[0]
  data = np.concatenate((data,tmpdat))

# plot the stuff
fig = figure(figsize=(float(figparms['Xlen']),float(figparms['Ylen'])))
plotopt = figopts['plot']
kmin = 0
for k in range(knum):
  kmax = lens[k] + kmin
  if plotopt == 'a':
    plot(data[kmin:kmax,0], data[kmin:kmax,1], klines[str(k)], color=kcolors[str(k)], label=klabs[str(k)], zorder=int(korders[str(k)]))
  elif plotopt == 'b':
    semilogy(data[kmin:kmax,0], data[kmin:kmax,1], klines[str(k)], color=kcolors[str(k)], label=klabs[str(k)], zorder=int(korders[str(k)]))
  elif plotopt == 'c':
    loglog(data[kmin:kmax,0], data[kmin:kmax,1], klines[str(k)], color=kcolors[str(k)], label=klabs[str(k)], zorder=int(korders[str(k)]))
  else:
    print 'figopts[plot] not recognized!'
    print 'figopts[plot] =',plotopt
    print 'exiting...'
    exit()
  kmin = kmax

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
if figopts['esci'] == 'on':
  ticklabel_format(style='sci', useMathText=True)  # to put scale from 'e' notation to scientific, if applicable
tick_params(labelsize=float(FS['tickfs']), which='both', direction='in', left=True, bottom=True, top=True, right=True)
xlabel(figparms['Xlab'], fontsize=float(FS['Xlabfs']))
ylabel(figparms['Ylab'], fontsize=float(FS['Ylabfs']))
legend(fontsize=float(FS['legfs']), loc=figparms['legpos'], fancybox=False, edgecolor='black')
tight_layout()


savefig(filename)
show()

