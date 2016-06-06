#!/usr/bin/python

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
import os


os.remove('min_energyQ20.list')

# get data
data = np.genfromtxt ('22-00_data.dat')
x0 = data[:,0]
t0 = data[:,1]
y0 = data[:,2]
z0 = data[:,4]

xi = 1

comparez = ones(5)

file = open("min_energyQ20.list", "w")

while xi <= 315:
   yvec = y0[(abs(x0-xi) <= 0.5)]
   tvec = t0[(abs(x0-xi) <= 1.0)]
   zvec = z0[(abs(x0-xi) <= 0.5)]
   zi = zvec.min()
   yi = yvec[(zvec == zvec.min())]
   ti = tvec[(zvec == zvec.min())]

   file.write(str(xi) + "		" + str(ti[0]) + "		" + str(yi[0]) + "		" + str(zi) + "\n")

   xi = xi+4

file.close()

# get data
data = np.genfromtxt ('min_energyQ20.list')
X0 = data[:,0]
Y0 = data[:,3]

data = np.genfromtxt ('min_energyQ20-fusion.list')
X1 = data[:,0]
Y1 = data[:,3]

maxY0 = Y0.max ();
minY0 = Y0.min ();

Y0 = Y0-minY0
Y1 = Y1-minY0
maxY0 = Y0.max ();
minY0 = Y0.min ();

# APS required dpi, figsize can change
fig = plt.figure (figsize = (6.0 , 6.0) , dpi = 1200)

# add a plot on the figure
ax = fig.add_subplot (111)

# set labels
ax.set_xlabel (r"$ {Q}_{20} (\rm{b}) $" , fontsize=20)
ax.set_ylabel (r"$ {E-E}_{0} (\rm{MeV}) $" , fontsize=20)

# set ticks (min, max, step) gives: [min , min+step , ... , max-step]
tab_range = np.arange (0.0, 415.0, 50.0)
ax.xaxis.set_ticks (tab_range)
#tab_range = np.arange (0.0, 35.0, 10.0)
#ax.yaxis.set_ticks (tab_range)

matplotlib.rc ('text', usetex=True)

origin = 'lower'
plt.plot (X0 , Y0, 'bo-')
plt.plot (X1 , Y1, 'ro--')
plt.title('Minimum energy profile')


fig.savefig ('min_energy-Q20-fissionfusion.ps')
