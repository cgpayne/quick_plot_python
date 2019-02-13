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

def ParseFile(fname, colmX, colmY, scaleX, scaleY, optX, optY):
  tmpmat = []
  with open(fname) as f:
    for line in f:
      if '#' in line: continue
      tmpmat.append(line.split())
  tmpmat = np.array(tmpmat)
  tmpmat = tmpmat[:,[colmX,colmY]]
  data = np.zeros(tmpmat.shape)
  for i in range(data.shape[0]):
    if optX == 'a':
      data[i,0] = scaleX*float(tmpmat[i,0])
    elif optX == 'b':
      data[i,0] = abs(scaleX*float(tmpmat[i,0]))
    else:
      print 'optX not recognized!'
      print 'fname =',fname
      print 'optX =',optX
      print 'exiting...'
      exit()
    if optY == 'a':
      data[i,1] = scaleY*float(tmpmat[i,1])
    elif optY == 'b':
      data[i,1] = abs(scaleY*float(tmpmat[i,1]))
    else:
      print 'optY not recognized!'
      print 'fname =',fname
      print 'optY =',optY
      print 'exiting...'
      exit()
  return data

#def hmin(array, string):
#  mins = []
#  for i in range(len(array)):
#    mins.append(min(array[i][string]))
#  return min(mins)

#def hmax(array, string):
#  maxes = []
#  for i in range(len(array)):
#    maxes.append(max(array[i][string]))
#  return max(maxes)


# set-up the config
Config = ConfigParser.ConfigParser()
Config.optionxform=str  # this overrides the default case-insensitivity
Config.read(confile)
figparms = ConfigSectionMap('figparms')  ## figure parameters/options
xylims = ConfigSectionMap('xylims')      ## limits for the plot
FS = ConfigSectionMap('FS')              ## font sizes
kfiles = ConfigSectionMap('kfiles')      ## data input files for each curve
klabs = ConfigSectionMap('klabs')        ## the labels for each curve
kcolms = ConfigSectionMap('kcolms')      ## data input file column parsing for each curve
kscales = ConfigSectionMap('kscales')    ## X and Y scale factors for each curve
kopts = ConfigSectionMap('kopts')        ## further options for X- and Y-data for each curve
klines = ConfigSectionMap('klines')      ## the line-type for each curve
kcolors = ConfigSectionMap('kcolors')    ## the colour for each curve
korders = ConfigSectionMap('korders')    ## the zorder for each curve

# some pre-formatting
if figparms['tex'] == 'on':
  matplotlib.rcParams['mathtext.fontset'] = 'stix'    # this is to switch to latex font style
  matplotlib.rcParams['font.family'] = 'STIXGeneral'  # " " " " " " " "

# parse the files for the data
knum = int(figparms['knum'])
data = np.zeros((0,2))
lens = np.zeros(knum, dtype=np.int)
for k in range(knum):
  kX = str(k) + 'X'
  kY = str(k) + 'Y'
  tmpdat = ParseFile(kfiles[str(k)], int(kcolms[kX]), int(kcolms[kY]), float(kscales[kX]), float(kscales[kY]), kopts[kX], kopts[kY])
  lens[k] = np.shape(tmpdat)[0]
  data = np.concatenate((data,tmpdat))

# plot the stuff
fig = figure(figsize=(float(figparms['Xlen']),float(figparms['Ylen'])))
plotopt = figparms['plot']
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
    print 'figparms[plot] not recognized!'
    print 'figparms[plot] =',plotopt
    print 'exiting...'
    exit()
  kmin = kmax

# set the limits
if xylims['xyauto'] == 'on':
  xdel = float(xylims['xdel'])
  ydel = float(xylims['ydel'])
  xlim(min(data[:,0])-xdel, max(data[:,0])+xdel)
  ylim(min(data[:,1])-ydel, max(data[:,1])+ydel)
else:
  xlim(float(xylims['xmin']), float(xylims['xmax']))
  ylim(float(xylims['ymin']), float(xylims['ymax']))

# other formatting
if figparms['esci'] == 'on':
  ticklabel_format(style='sci', useMathText=True)  # to put scale from 'e' notation to scientific, if applicable
tick_params(labelsize=float(FS['tickfs']), which='both', direction='in', left=True, bottom=True, top=True, right=True)
xlabel(figparms['Xlab'], fontsize=float(FS['Xlabfs']))
ylabel(figparms['Ylab'], fontsize=float(FS['Ylabfs']))
legend(fontsize=float(FS['legfs']), loc=figparms['legpos'], fancybox=False, edgecolor='black')
tight_layout()


savefig(filename)
show()

