#!/usr/bin/python


## for LaTeX in the .ps
import matplotlib
matplotlib.use ('PS')
from matplotlib import rc
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
# to have ascii hyphen minus signs (shorter than the official unicode)
matplotlib.rcParams['text.latex.unicode']=False
matplotlib.rc ('font',**{'family':'serif','serif':['Times'] , 'size':20})

from matplotlib.pyplot import figure , axes , plot , xlabel , ylabel , title , grid , savefig , show
import numpy as np
from pylab import *

import matplotlib.pyplot as plt
from matplotlib.pyplot import axhline


set_printoptions(threshold=nan)


infile = 'local_000001.out'
#infile = raw_input("\n Please list the name of the input file containing the density information (typically densi_[something].out): \n Columns should be ordered x, y, z, rho_p, rho_n, rho_tot. \n")


############################################################################

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

############################################################################



x0, y0, z0, loc_up, loc_down = [], [], [], [], []

# get data
with open(infile) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'NEUTRON LOCALIZATION':  # Or whatever test is needed
            break
    # Reads text until the end of the block:
    for line in input_data:  # This keeps reading the file
        if line.strip() == 'PROTON LOCALIZATION':
            break
        floats = [float(x) for x in line.split()]
        x0.append(floats[0])
        z0.append(floats[1])
        y0.append(floats[2])
        loc_up.append(floats[3])
        loc_down.append(floats[4])

x0 = np.asarray(x0)
y0 = np.asarray(y0)
z0 = np.asarray(z0)
loc_up = np.asarray(loc_up)
loc_down = np.asarray(loc_down)

# Take a single cross-sectional slice of the total 3D density
zslice = min([abs(z) for z in z0])
print zslice
xpos = x0[(z0 == zslice) & (x0 > 0)]
xneg = x0[(z0 == zslice) & (x0 < 0)]
ypos = y0[(z0 == zslice) & (x0 > 0)]
yneg = y0[(z0 == zslice) & (x0 < 0)]
loc_uppos = loc_up[(z0 == zslice) & (x0 > 0)]
loc_downpos = loc_down[(z0 == zslice) & (x0 > 0)]
loc_upneg = loc_uppos[::-1]
loc_downneg = loc_downpos[::-1]

nans, x= nan_helper(loc_uppos)
loc_uppos[nans]= np.interp(x(nans), x(~nans), loc_uppos[~nans])

x0 = np.concatenate((xpos, xneg), axis=0)
y0 = np.concatenate((ypos, yneg[::-1]), axis=0)
loc_up = np.concatenate((loc_uppos, loc_upneg), axis=0)
loc_down = np.concatenate((loc_downpos, loc_downneg), axis=0)

# basis grid for the interpolation
xi = np.linspace (min (x0) , max (x0))
yi = np.linspace (min (y0) , max (y0))

# interpolate data
X0, Y0 = np.meshgrid (xi , yi)
Z0 = griddata (x0 , y0 , loc_up , xi , yi)

# get Z max and min to set the plot
maxZ0 = Z0.max ();
minZ0 = Z0.min ();
print maxZ0
print minZ0


# APS required dpi, figsize can change
fig = plt.figure (figsize = (6.0 , 6.0) , dpi = 1200)

# add a plot on the figure
ax = fig.add_subplot (111)


# set labels
ax.set_xlabel (r"$ x (\rm{fm}) $" , fontsize=20)
ax.set_ylabel (r"$ y (\rm{fm}) $" , fontsize=20)

# set ticks (min, max, step) gives: [min , min+step , ... , max-step]
rangemax = max(round(X0.max()),round(Y0.max()))
rangemin = min(round(X0.min()),round(Y0.min()))
tab_range = np.arange (-15, rangemax, 5.0)
#tab_range = np.arange (0.0, 9.0, 3.0)
ax.xaxis.set_ticks (tab_range)
ax.yaxis.set_ticks (tab_range)

plt.axis('equal')

origin = 'lower'
CS0 = plt.contourf (X0 , Y0 , Z0 , 100 , origin=origin , vmin=minZ0 , vmax=maxZ0, cmap=plt.cm.jet)


############
# colorbar #
############
# compress the figure to make some room for the colorbar
fig.subplots_adjust (right=0.88)

# set the colorbar position and size
# [distance to the z axis , height from the bottom , width of the bar , length of the bar]
cbar_ax = fig.add_axes ([0.9 , 0.1 , 0.04 , 0.8])

# ticks along the colorbar
#step = 5
#decimal_number = 2#-1
#v = np.linspace (round (minZ0 , decimal_number) , round (maxZ0 + (maxZ0-minZ0)/step , decimal_number) , step , endpoint=True).tolist ()
#v = [round (elem , decimal_number) for elem in v] # warning, these are positions of ticks, the "round" function can lead to irregular spacings
v = [0.0, 0.25, 0.5, 0.75, 1.0]

#wait = raw_input("PRESS ENTER TO CONTINUE.")

# plot the colorbar
#cb = plt.colorbar (CS0 , cax=cbar_ax , ticks=v , norm=matplotlib.colors.Normalize (vmin=minZ0 , vmax=maxZ0))
cb = plt.colorbar (CS0 , cax=cbar_ax , ticks=v , norm=matplotlib.colors.Normalize (vmin=0.0 , vmax=1.0))


# to get scientific notation (conflict with APS font)
matplotlib.rcParams['axes.unicode_minus'] = True
cb.formatter.set_powerlimits ((-2 , 2))
cb.update_ticks ()


# hide the exponent generated by the scientific notation
# conflict with internal LaTeX routines
# look at the maxZ0 which is printed at the execution, look at the colorbar ticks and deduce the exponent
# then add it in the label definition (APS recommended: "x (10^2 fm)")
cb.ax.get_yaxis ().get_offset_text ().set_visible (False)
############

text(0.1, 0.9, r'$\rho_n$',
    horizontalalignment='center',
    verticalalignment='center',
    transform = ax.transAxes)


# to call external LaTeX libraries for dealing with latex command not included in python
# will produce conflicts if called before
matplotlib.rc ('text', usetex=True)


# to add some text on the graph
# not tested
#ax.text (9 , 0 , 0 , "toto" , color='red')
#ax.annotate(r"$ \boldsymbol{ {1/2}^{+} } $" , xy=(6.3 , 6.5) , color='white' , ha='center' , fontsize=23)


# save in ps format, cannot be donne directly in pdf and eps has no bounding box
# follow the instruction below to get a pdf with bounding box
fig.savefig ('176Pt-285018n-locali.ps')
# in the terminal:
# ps2eps -f test.ps ; epstopdf test.eps



###################################################
#### Now repeat the calculation for protons #######
###################################################

x0, y0, z0, loc_up, loc_down = [], [], [], [], []

# get data
with open(infile) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'PROTON LOCALIZATION':  # Or whatever test is needed
            break
    # Reads text until the end of the block:
    for line in input_data:  # This keeps reading the file
        if line.strip() == 'ALPHA LOCALIZATION':
            break
        floats = [float(x) for x in line.split()]
        x0.append(floats[0])
        z0.append(floats[1])
        y0.append(floats[2])
        loc_up.append(floats[3])
        loc_down.append(floats[4])

x0 = np.asarray(x0)
y0 = np.asarray(y0)
z0 = np.asarray(z0)
loc_up = np.asarray(loc_up)
loc_down = np.asarray(loc_down)

# Take a single cross-sectional slice of the total 3D density
zslice = min([abs(z) for z in z0])
print zslice
xpos = x0[(z0 == zslice) & (x0 > 0)]
xneg = x0[(z0 == zslice) & (x0 < 0)]
ypos = y0[(z0 == zslice) & (x0 > 0)]
yneg = y0[(z0 == zslice) & (x0 < 0)]
loc_uppos = loc_up[(z0 == zslice) & (x0 > 0)]
loc_downpos = loc_down[(z0 == zslice) & (x0 > 0)]
loc_upneg = loc_uppos[::-1]
loc_downneg = loc_downpos[::-1]

nans, x= nan_helper(loc_uppos)
loc_uppos[nans]= np.interp(x(nans), x(~nans), loc_uppos[~nans])

x0 = np.concatenate((xpos, xneg), axis=0)
y0 = np.concatenate((ypos, yneg[::-1]), axis=0)
loc_up = np.concatenate((loc_uppos, loc_upneg), axis=0)
loc_down = np.concatenate((loc_downpos, loc_downneg), axis=0)

# basis grid for the interpolation
xi = np.linspace (min (x0) , max (x0))
yi = np.linspace (min (y0) , max (y0))

# interpolate data
X0, Y0 = np.meshgrid (xi , yi)
Z0 = griddata (x0 , y0 , loc_up , xi , yi)

# get Z max and min to set the plot
maxZ0 = Z0.max ();
minZ0 = Z0.min ();
print maxZ0
print minZ0


# APS required dpi, figsize can change
fig = plt.figure (figsize = (6.0 , 6.0) , dpi = 1200)

# add a plot on the figure
ax = fig.add_subplot (111)


# set labels
ax.set_xlabel (r"$ x (\rm{fm}) $" , fontsize=20)
ax.set_ylabel (r"$ y (\rm{fm}) $" , fontsize=20)

# set ticks (min, max, step) gives: [min , min+step , ... , max-step]
ax.xaxis.set_ticks (tab_range)
ax.yaxis.set_ticks (tab_range)

plt.axis('equal')

origin = 'lower'
CS0 = plt.contourf (X0 , Y0 , Z0 , 100 , origin=origin , vmin=minZ0 , vmax=maxZ0, cmap=plt.cm.jet)


############
# colorbar #
############
# compress the figure to make some room for the colorbar
fig.subplots_adjust (right=0.88)

# set the colorbar position and size
# [distance to the z axis , height from the bottom , width of the bar , length of the bar]
cbar_ax = fig.add_axes ([0.9 , 0.1 , 0.04 , 0.8])

# ticks along the colorbar
#step = 5
#decimal_number = 2#-1
#v = np.linspace (round (minZ0 , decimal_number) , round (maxZ0 + (maxZ0-minZ0)/step , decimal_number) , step , endpoint=True).tolist ()
#v = [round (elem , decimal_number) for elem in v] # warning, these are positions of ticks, the "round" function can lead to irregular spacings
v = [0.0, 0.25, 0.5, 0.75, 1.0]

#wait = raw_input("PRESS ENTER TO CONTINUE.")

# plot the colorbar
#cb = plt.colorbar (CS0 , cax=cbar_ax , ticks=v , norm=matplotlib.colors.Normalize (vmin=minZ0 , vmax=maxZ0))
cb = plt.colorbar (CS0 , cax=cbar_ax , ticks=v , norm=matplotlib.colors.Normalize (vmin=0.0 , vmax=1.0))


# to get scientific notation (conflict with APS font)
matplotlib.rcParams['axes.unicode_minus'] = True
cb.formatter.set_powerlimits ((-2 , 2))
cb.update_ticks ()


# hide the exponent generated by the scientific notation
# conflict with internal LaTeX routines
# look at the maxZ0 which is printed at the execution, look at the colorbar ticks and deduce the exponent
# then add it in the label definition (APS recommended: "x (10^2 fm)")
cb.ax.get_yaxis ().get_offset_text ().set_visible (False)
############

text(0.1, 0.9, r'$\rho_p$',
    horizontalalignment='center',
    verticalalignment='center',
    transform = ax.transAxes)


# to call external LaTeX libraries for dealing with latex command not included in python
# will produce conflicts if called before
matplotlib.rc ('text', usetex=True)


# to add some text on the graph
# not tested
#ax.text (9 , 0 , 0 , "toto" , color='red')
#ax.annotate(r"$ \boldsymbol{ {1/2}^{+} } $" , xy=(6.3 , 6.5) , color='white' , ha='center' , fontsize=23)


# save in ps format, cannot be donne directly in pdf and eps has no bounding box
# follow the instruction below to get a pdf with bounding box
fig.savefig ('176Pt-285018p-locali.ps')
# in the terminal:
# ps2eps -f test.ps ; epstopdf test.eps
