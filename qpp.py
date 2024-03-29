#!/usr/bin/env python
##  head -n 18 qpp.py
##  python qpp.py config.in output_plot.pdf
##  By: Charlie Payne, 2018-2019
## DESCRIPTION
##  this is basically a proto-wrapper for matplotlib to do a quick plot via python
##  that said, to make it convenient it's become more of a beast than I had originally intended
##  and it may very well make a good basis for publishable figures, anyone's welcome to use it!
##  it should make some sense, especially in combination with reading the default config.in (entry names are moderately intuitive)
## KNOWN BUGS
##  [none]
## DESIRED FEATURES
##  -- add in formatter for input data
##  -- convert to python3 and flake8 standards
##  -- it would be nice to somehow have default values for the 'kscales' and alike, for now rely on default config.in
##  -- somehow generalize kopts such that the user can use any general python function on the data
##  -- maybe automate a line border
##  -- add in error bar plotting
##  -- somehow make a sub-figure setup... :|
## PARAMETERS
##  1) confile = sys.argv[1]     # the plotting config file, see 'config.in' for the default structure
##  2) filename = sys.argv[2]    # pdf output file name (including desired extension)

import sys
import ConfigParser
from matplotlib.pylab import *

confile = sys.argv[1]     # the plotting config file, see 'config.in' for the default structure
filename = sys.argv[2]    # pdf output file name (including desired extension)



# ~~~ function definitions ~~~

# in:   section = section name in the config file, where they're designated by square brackets []
# out:  dict1 = a python dictionary filled with the config information
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

# in:   knum = curve number - 1, fname = filename, colX/Y = colm in file to use for X/Y-axis
#         scaleX/Y = scaling factor for X/Y-data, optX/Y = see 'kopts' in config.in
# out:  nparr = numpy array[N,2] with X- and Y-data based on the above settings
def ParseFile(knum, fname, colmX, colmY, scaleX, scaleY, optX, optY):
  tmpmat = []  # I could probably do this part better, but it works!
  with open(fname) as f:
    for line in f:
      if '#' in line: continue  # skip commented out lines
      tmpmat.append(line.split())
  tmpmat = np.array(tmpmat)
  tmpmat = tmpmat[:,[colmX,colmY]]  # strip the data
  nparr = np.zeros(tmpmat.shape)
  for i in range(nparr.shape[0]):
    if optX == 'def':
      nparr[i,0] = scaleX*float(tmpmat[i,0])
    elif optX == 'abs':
      nparr[i,0] = scaleX*abs(float(tmpmat[i,0]))
    else:
      print 'ERROR 6872: kopts[%iX] not recognized!'%(knum)
      print 'kopts[%iX] = %s'%(knum,optX)
      print 'exiting...'
      exit()
    if optY == 'def':
      nparr[i,1] = scaleY*float(tmpmat[i,1])
    elif optY == 'abs':
      nparr[i,1] = scaleY*abs(float(tmpmat[i,1]))
    else:
      print 'ERROR 7656: kopts[%iY] not recognized!'%(knum)
      print 'kopts[%iY] = %s'%(knum,optY)
      print 'exiting...'
      exit()
  return nparr



# --------- execute the code ---------

# set-up the config, grab the respective dictionaries
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
kwidths = ConfigSectionMap('kwidths')    ## the line-width for each curve
kcolors = ConfigSectionMap('kcolors')    ## the colour for each curve
kalphas = ConfigSectionMap('kalphas')    ## the alpha (transparency) for each curve
korders = ConfigSectionMap('korders')    ## the zorder for each curve

# some pre-formatting
if figparms['tex'] == 'on':
  matplotlib.rcParams['mathtext.fontset'] = 'stix'    # this is to switch to latex font style
  matplotlib.rcParams['font.family'] = 'STIXGeneral'  # " " " " " " " "

# parse the files for the data
knum = int(figparms['knum'])
data = np.zeros((0,2))  # will hold all the data in one concatenated array, curve by curve...
lens = np.zeros(knum, dtype=np.int)  # will hold the number of points (lengths) in the data for each curve
for k in range(knum):
  kX = str(k) + 'X'
  kY = str(k) + 'Y'
  tmpdat = ParseFile(k, kfiles[str(k)], int(kcolms[kX]), int(kcolms[kY]), float(kscales[kX]), float(kscales[kY]), kopts[kX], kopts[kY])
  lens[k] = np.shape(tmpdat)[0]
  data = np.concatenate((data,tmpdat))  # concatenate data from each curve into one array

# plot the stuff
fig = figure(figsize=(float(figparms['Xlen']),float(figparms['Ylen'])))
axesopt = figparms['axes']  # see 'figparms' in config.in
kmin = 0  # the lower-bound index for the data points per curve in the concatenated array 'data'
for k in range(knum):
  kmax = lens[k] + kmin  # the upper-bound index " " " " " " " " " " "
  if axesopt == 'linear':
    plot(data[kmin:kmax,0], data[kmin:kmax,1], klines[str(k)], color=kcolors[str(k)], label=klabs[str(k)],
      linewidth=float(kwidths[str(k)]), alpha=float(kalphas[str(k)]), zorder=float(korders[str(k)]))
  elif axesopt == 'semilogy':
    semilogy(data[kmin:kmax,0], data[kmin:kmax,1], klines[str(k)], color=kcolors[str(k)], label=klabs[str(k)],
      linewidth=float(kwidths[str(k)]), alpha=float(kalphas[str(k)]), zorder=float(korders[str(k)]))
  elif axesopt == 'semilogx':
    semilogx(data[kmin:kmax,0], data[kmin:kmax,1], klines[str(k)], color=kcolors[str(k)], label=klabs[str(k)],
      linewidth=float(kwidths[str(k)]), alpha=float(kalphas[str(k)]), zorder=float(korders[str(k)]))
  elif axesopt == 'loglog':
    loglog(data[kmin:kmax,0], data[kmin:kmax,1], klines[str(k)], color=kcolors[str(k)], label=klabs[str(k)],
      linewidth=float(kwidths[str(k)]), alpha=float(kalphas[str(k)]), zorder=float(korders[str(k)]))
  else:
    print 'ERROR 0798: figparms[axes] not recognized!'
    print 'figparms[axes] =',axesopt
    print 'exiting...'
    exit()
  kmin = kmax  # don't forget to update in the concatenation, see!

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
  ticklabel_format(style='sci', useMathText=True)  # to put scale from base-e notation to scientific, if applicable
tick_params(labelsize=float(FS['tickfs']), which='both', direction='in', left=True, bottom=True, top=True, right=True)
xlabel(figparms['Xlab'], fontsize=float(FS['Xlabfs']))
ylabel(figparms['Ylab'], fontsize=float(FS['Ylabfs']))
if figparms['legt'] == 'on':
  legend(fontsize=float(FS['legfs']), loc=figparms['legpos'], fancybox=False, edgecolor='black')
else:
  legend(fontsize=float(FS['legfs']), loc=figparms['legpos'], fancybox=False, edgecolor='black', framealpha=1)
tight_layout(pad=float(figparms['pad']), w_pad=0, h_pad=0)  # I guess the w/h_pad will make more sense once I do subplots..?

# finalize
savefig(filename)
if figparms['show'] == 'on':
  show()  # if you want to edit the figure from the window, put this before savefig (I guess that's possible..?)



## FIN
