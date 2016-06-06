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


os.remove('min_energyQ30.list')

# get data
data = np.genfromtxt ('outputs.dat')
x0 = data[:,0]
t0 = data[:,1]
y0 = data[:,2]
z0 = data[:,4]

yi = 0

comparez = ones(5)

file = open("min_energyQ30.list", "w")

while yi <= 30:
   xvec = x0[(abs(y0-yi) <= 0.5) & (x0<260)]
   tvec = t0[(abs(y0-yi) <= 1.0) & (x0<260)]
   zvec = z0[(abs(y0-yi) <= 0.5) & (x0<260)]
   zi = zvec.min()
   xi = xvec[(zvec == zvec.min())]
   ti = tvec[(zvec == zvec.min())]

   file.write(str(xi[0]) + "		" + str(ti[0]) + " 		" + str(yi) + " 		" + str(zi) + "\n")

   yi = yi+2

file.close()

# get data
data = np.genfromtxt ('min_energyQ30.list')
X0 = data[:,2]
Y0 = data[:,3]

maxY0 = Y0.max ();
minY0 = -1430.13211279; #Y0.min ();

Y0 = Y0-minY0
maxY0 = Y0.max ();
minY0 = Y0.min ();

# APS required dpi, figsize can change
fig = plt.figure (figsize = (6.0 , 6.0) , dpi = 1200)

# add a plot on the figure
ax = fig.add_subplot (111)

# set labels
ax.set_xlabel (r"$ {Q}_{30} (\rm{b}^\frac{3}{2}) $" , fontsize=20)
ax.set_ylabel (r"$ {E-E}_{0} (\rm{MeV}) $" , fontsize=20)

# set ticks (min, max, step) gives: [min , min+step , ... , max-step]
tab_range = np.arange (0.0, 35.0, 5.0)
ax.xaxis.set_ticks (tab_range)
#tab_range = np.arange (0.0, 35.0, 10.0)
#ax.yaxis.set_ticks (tab_range)

matplotlib.rc ('text', usetex=True)

origin = 'lower'
plt.scatter (X0 , Y0)
plt.title('Minimum energy profile')


fig.savefig ('min_energy-Q30.ps')
