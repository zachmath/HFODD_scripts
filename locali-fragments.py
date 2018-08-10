#!/usr/bin/python


## for LaTeX in the .ps
import matplotlib
matplotlib.use ('PS')
from matplotlib import rc
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
# to have ascii hyphen minus signs (shorter than the official unicode)
matplotlib.rcParams['text.latex.unicode']=False
matplotlib.rc ('font',**{'family':'serif','serif':['Times New Roman'] , 'size':30})
matplotlib.rc ('text', usetex=True)


from matplotlib.pyplot import figure , axes , plot , xlabel , ylabel , title , grid , savefig , show
import numpy as np
from pylab import *

import matplotlib.pyplot as plt
from matplotlib.pyplot import axhline


set_printoptions(threshold=nan)


infile0 = 'locali-208Pb.out' # Left (larger?) fragment 
infile1 = 'local_86Kr-pre.out' # Right fragment
infile2 = 'local_264060.out'
offset0 = 4.25#4.3
offset1 = 10.5

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



x0, y0, z0, loc_up0, loc_down0 = [], [], [], [], []
x1, y1, z1, loc_up1, loc_down1 = [], [], [], [], []
x2, y2, z2, loc_up2, loc_down2 = [], [], [], [], []

# get data
with open(infile0) as input_data:
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
        loc_up0.append(floats[3])
        loc_down0.append(floats[4])
with open(infile1) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'NEUTRON LOCALIZATION':  # Or whatever test is needed
            break
    # Reads text until the end of the block:
    for line in input_data:  # This keeps reading the file
        if line.strip() == 'PROTON LOCALIZATION':
            break
        floats = [float(x) for x in line.split()]
        x1.append(floats[0])
        z1.append(floats[1])
        y1.append(floats[2])
        loc_up1.append(floats[3])
        loc_down1.append(floats[4])
with open(infile2) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'NEUTRON LOCALIZATION':  # Or whatever test is needed
            break
    # Reads text until the end of the block:
    for line in input_data:  # This keeps reading the file
        if line.strip() == 'PROTON LOCALIZATION':
            break
        floats = [float(x) for x in line.split()]
        x2.append(floats[0])
        z2.append(floats[1])
        y2.append(floats[2])
        loc_up2.append(floats[3])
        loc_down2.append(floats[4])

x0 = np.asarray(x0)
y0 = np.asarray(y0)
y0= y0-offset0
z0 = np.asarray(z0)
loc_up0 = np.asarray(loc_up0)
loc_down0 = np.asarray(loc_down0)
xyzud0 = zip(x0, y0, z0, loc_up0, loc_down0)

x1 = np.asarray(x1)
y1 = np.asarray(y1)
y1= y1+offset1
#y1= -y1+offset1
z1 = np.asarray(z1)
loc_up1 = np.asarray(loc_up1)
loc_down1 = np.asarray(loc_down1)
xyzud1 = zip(x1, y1, z1, loc_up1, loc_down1)

x2 = np.asarray(x2)
y2 = np.asarray(y2)
z2 = np.asarray(z2)
loc_up2 = np.asarray(loc_up2)
loc_down2 = np.asarray(loc_down2)
xyzud2 = zip(x2, y2, z2, loc_up2, loc_down2)

# Take a single cross-sectional slice of the total 3D density
zslice = min([abs(z) for z in z0])
xslice = min([abs(x) for x in x0])
print zslice
xyzud0 = [xyzud for xyzud in xyzud0 if xyzud[0]==xslice and xyzud[2]==zslice]
x0 = [xyzud[0] for xyzud in xyzud0]
y0 = [xyzud[1] for xyzud in xyzud0]
z0 = [xyzud[2] for xyzud in xyzud0]
loc_up0 = [xyzud[3] for xyzud in xyzud0]
loc_down0 = [xyzud[4] for xyzud in xyzud0]


zslice = min([abs(z) for z in z1])
xslice = min([abs(x) for x in x1])
print zslice
xyzud1 = [xyzud for xyzud in xyzud1 if xyzud[0]==xslice and xyzud[2]==zslice]
x1 = [xyzud[0] for xyzud in xyzud1]
y1 = [xyzud[1] for xyzud in xyzud1]
z1 = [xyzud[2] for xyzud in xyzud1]
loc_up1 = [xyzud[3] for xyzud in xyzud1]
loc_down1 = [xyzud[4] for xyzud in xyzud1]


zslice = min([abs(z) for z in z2])
xslice = min([abs(x) for x in x2])
print zslice
xyzud2 = [xyzud for xyzud in xyzud2 if xyzud[0]==xslice and xyzud[2]==zslice]
x2 = [xyzud[0] for xyzud in xyzud2]
y2 = [xyzud[1] for xyzud in xyzud2]
z2 = [xyzud[2] for xyzud in xyzud2]
loc_up2 = [xyzud[3] for xyzud in xyzud2]
loc_down2 = [xyzud[4] for xyzud in xyzud2]


# Set aside neutron data
y0n = y0
y1n = y1
y2n = y2
loc_up0n = loc_up0
loc_up1n = loc_up1
loc_up2n = loc_up2




###################################################
##### Now repeat collect the data for protons #####
###################################################

x0, y0, z0, loc_up0, loc_down0 = [], [], [], [], []
x1, y1, z1, loc_up1, loc_down1 = [], [], [], [], []
x2, y2, z2, loc_up2, loc_down2 = [], [], [], [], []

# get data
with open(infile0) as input_data:
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
        loc_up0.append(floats[3])
        loc_down0.append(floats[4])
with open(infile1) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'PROTON LOCALIZATION':  # Or whatever test is needed
            break
    # Reads text until the end of the block:
    for line in input_data:  # This keeps reading the file
        if line.strip() == 'ALPHA LOCALIZATION':
            break
        floats = [float(x) for x in line.split()]
        x1.append(floats[0])
        z1.append(floats[1])
        y1.append(floats[2])
        loc_up1.append(floats[3])
        loc_down1.append(floats[4])
with open(infile2) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'PROTON LOCALIZATION':  # Or whatever test is needed
            break
    # Reads text until the end of the block:
    for line in input_data:  # This keeps reading the file
        if line.strip() == 'ALPHA LOCALIZATION':
            break
        floats = [float(x) for x in line.split()]
        x2.append(floats[0])
        z2.append(floats[1])
        y2.append(floats[2])
        loc_up2.append(floats[3])
        loc_down2.append(floats[4])

x0 = np.asarray(x0)
y0 = np.asarray(y0)
y0= y0-offset0
z0 = np.asarray(z0)
loc_up0 = np.asarray(loc_up0)
loc_down0 = np.asarray(loc_down0)
xyzud0 = zip(x0, y0, z0, loc_up0, loc_down0)

x1 = np.asarray(x1)
y1 = np.asarray(y1)
y1= y1+offset1
#y1= -y1+offset1
z1 = np.asarray(z1)
loc_up1 = np.asarray(loc_up1)
loc_down1 = np.asarray(loc_down1)
xyzud1 = zip(x1, y1, z1, loc_up1, loc_down1)

x2 = np.asarray(x2)
y2 = np.asarray(y2)
z2 = np.asarray(z2)
loc_up2 = np.asarray(loc_up2)
loc_down2 = np.asarray(loc_down2)
xyzud2 = zip(x2, y2, z2, loc_up2, loc_down2)

# Take a single cross-sectional slice of the total 3D density
zslice = min([abs(z) for z in z0])
xslice = min([abs(x) for x in x0])
print zslice
xyzud0 = [xyzud for xyzud in xyzud0 if xyzud[0]==xslice and xyzud[2]==zslice]
x0 = [xyzud[0] for xyzud in xyzud0]
y0 = [xyzud[1] for xyzud in xyzud0]
z0 = [xyzud[2] for xyzud in xyzud0]
loc_up0 = [xyzud[3] for xyzud in xyzud0]
loc_down0 = [xyzud[4] for xyzud in xyzud0]


zslice = min([abs(z) for z in z1])
xslice = min([abs(x) for x in x1])
print zslice
xyzud1 = [xyzud for xyzud in xyzud1 if xyzud[0]==xslice and xyzud[2]==zslice]
x1 = [xyzud[0] for xyzud in xyzud1]
y1 = [xyzud[1] for xyzud in xyzud1]
z1 = [xyzud[2] for xyzud in xyzud1]
loc_up1 = [xyzud[3] for xyzud in xyzud1]
loc_down1 = [xyzud[4] for xyzud in xyzud1]


zslice = min([abs(z) for z in z2])
xslice = min([abs(x) for x in x2])
print zslice
xyzud2 = [xyzud for xyzud in xyzud2 if xyzud[0]==xslice and xyzud[2]==zslice]
x2 = [xyzud[0] for xyzud in xyzud2]
y2 = [xyzud[1] for xyzud in xyzud2]
z2 = [xyzud[2] for xyzud in xyzud2]
loc_up2 = [xyzud[3] for xyzud in xyzud2]
loc_down2 = [xyzud[4] for xyzud in xyzud2]


# Set aside proton data
y0p = y0
y1p = y1
y2p = y2
loc_up0p = loc_up0
loc_up1p = loc_up1
loc_up2p = loc_up2

############## Actual plotting begins here #########################

fig = plt.figure(figsize = (6,6) , dpi = 1200)

ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)

# set x ticks
minorLocator = MultipleLocator(5)
majorLocator = MultipleLocator(15)
ax1.xaxis.set_minor_locator(minorLocator)
ax1.xaxis.set_major_locator(majorLocator)
ax2.xaxis.set_minor_locator(minorLocator)
ax2.xaxis.set_major_locator(majorLocator)

ax1.set_xlim((-20,20))
ax2.set_xlim((-20,20))

# set y ticks
minorLocator = MultipleLocator(0.05)
majorLocator = MultipleLocator(0.25)
ax1.yaxis.set_minor_locator(minorLocator)
ax1.yaxis.set_major_locator(majorLocator)
ax2.yaxis.set_minor_locator(minorLocator)
ax2.yaxis.set_major_locator(majorLocator)

ax1.set_ylim((0,0.85))
ax2.set_ylim((0,0.85))

ax2.set_yticklabels([])

ax1.set_aspect(40.0/0.85*.8)
ax2.set_aspect(40.0/0.85*.8)

# plot the things
origin = 'lower'
ax1.plot (y0n , loc_up0n , 'g--', label='$^{208}$Pb')
ax1.plot (y1n , loc_up1n , 'b--', label='$^{86}$Kr')
ax1.plot (y2n , loc_up2n , 'r:')

origin = 'lower'
ax2.plot (y0p , loc_up0p , 'g--', label='$^{208}$Pb')
ax2.plot (y1p , loc_up1p , 'b--', label='$^{86}$Kr')
ax2.plot (y2p , loc_up2p , 'r:')

# label each box
ax1.text(-2,0.91,r'$\mathcal{C}_n$',color='black')
ax2.text(-2,0.91,r'$\mathcal{C}_p$',color='black')

# label the fragment curves
ax2.text(-10,0.15,r'$^{208}$Pb',color='g',fontsize=20)
ax2.text( 6,0.15,r'$^{96}$Kr',color='b',fontsize=20)

# set labels
fig.text(0.5, 0.20, r'z (fm)', ha='center')
#ax1.set_ylabel (r"$ NLF $" , fontsize=20)

# to call external LaTeX libraries for dealing with latex command not included in python
# will produce conflicts if called before
matplotlib.rc ('text', usetex=True)
fig.subplots_adjust(wspace=0.0, hspace=0.0)


fig.savefig ('294Og-with_frags.ps')

