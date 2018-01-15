#!/usr/bin/python

## for LaTeX in the .ps
import matplotlib
matplotlib.use ('PS')
from matplotlib import rc

matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}", r'\DeclareMathAlphabet\mathcal{OMS}{cmsy}{m}{n}']
matplotlib.rcParams['axes.unicode_minus']=False
matplotlib.rc ('font',**{'family':'serif','serif':['Times'] , 'size':20})


from matplotlib.pyplot import figure , axes , plot , xlabel , ylabel , title , grid , savefig , show
import numpy as np
from pylab import *

import matplotlib.pyplot as plt
from matplotlib.pyplot import axhline

from matplotlib.gridspec import GridSpec
import matplotlib.gridspec as gridspec



import warnings
import scipy.interpolate
import random
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.font_manager import FontProperties
import matplotlib.colors as mcolors

set_printoptions(threshold=nan)
def make_colormap(seq):
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)
  
c = mcolors.ColorConverter().to_rgb
maplinear = make_colormap([c('white'),c('blue'),0.2, c('blue'), c('cyan'), 0.4, c('cyan'), c('green'), 0.6, c('green'), c('yellow'), 0.8, c('yellow'), c('red')])


####################################################################################

fontsize=20

N = 100
#levels1 = np.linspace(0, 0.10, 50)
levels2 = np.linspace(0, 1.0, 200)

x1n,z1n,neu_up1 = np.genfromtxt(r'local_neu_up_61-0.out',unpack=True,skip_header=0)
x1n,z1n,neu_dw1 = np.genfromtxt(r'local_neu_dw_61-0.out',unpack=True,skip_header=0)
x1p,z1p,pro_up1 = np.genfromtxt(r'local_pro_up_61-0.out',unpack=True,skip_header=0)
x1p,z1p,pro_dw1 = np.genfromtxt(r'local_pro_dw_61-0.out',unpack=True,skip_header=0)

x2n,z2n,neu_up2 = np.genfromtxt(r'local_neu_up_149-0.out',unpack=True,skip_header=0)
x2n,z2n,neu_dw2 = np.genfromtxt(r'local_neu_up_149-14.out',unpack=True,skip_header=0)
x2p,z2p,pro_up2 = np.genfromtxt(r'local_pro_up_149-0.out',unpack=True,skip_header=0)
x2p,z2p,pro_dw2 = np.genfromtxt(r'local_pro_up_149-14.out',unpack=True,skip_header=0)

x3n,z3n,neu_up3 = np.genfromtxt(r'local_neu_up_229-0.out',unpack=True,skip_header=0)
x3n,z3n,neu_dw3 = np.genfromtxt(r'local_neu_up_229-24.out',unpack=True,skip_header=0)
x3p,z3p,pro_up3 = np.genfromtxt(r'local_pro_up_229-0.out',unpack=True,skip_header=0)
x3p,z3p,pro_dw3 = np.genfromtxt(r'local_pro_up_229-24.out',unpack=True,skip_header=0)

x4n,z4n,neu_up4 = np.genfromtxt(r'local_neu_up_249-0.out',unpack=True,skip_header=0)
x4n,z4n,neu_dw4 = np.genfromtxt(r'local_neu_up_249-24.out',unpack=True,skip_header=0)
x4p,z4p,pro_up4 = np.genfromtxt(r'local_pro_up_249-0.out',unpack=True,skip_header=0)
x4p,z4p,pro_dw4 = np.genfromtxt(r'local_pro_up_249-24.out',unpack=True,skip_header=0)


####################################################################################
def rho_plot(ax,r,z,rho):
#   do the interpolation with cubic method
    ri = np.linspace(r.min(), r.max(), N)
    zi = np.linspace(z.min(), z.max(), N)
    rhoi = scipy.interpolate.griddata((r, z), rho, (ri[None,:], zi[:,None]), method='linear')
    

    ax.set_xlim((-10,10))
    ax.set_ylim((-15,15))

    minorLocator = MultipleLocator(5)
    majorLocator = MultipleLocator(10)
    ax.yaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_major_locator(majorLocator)
    
    ax.xaxis.set_ticks(np.arange(-5, 6, 5))
    
    for ticks in ax.xaxis.get_ticklines() + ax.yaxis.get_ticklines(minor=True) + ax.yaxis.get_ticklines(minor=False):
        ticks.set_color('k')
    for pos in ['top', 'bottom', 'right', 'left']:
        ax.spines[pos].set_edgecolor('k')
    
    cs1 = ax.contourf(ri,zi,rhoi,100,cmap=plt.cm.gnuplot) #YlGnBu
    #cs2 = ax.contour(ri,zi,rhoi,5,colors='0.75',hold='on')

    if ax == ax15:
        cb1 = plt.colorbar(cs1,cax = cbaxes1,ticks=[0.0,0.05,0.10],format='%.2f',orientation='vertical')
        labels=[l.get_text() for l in cb1.ax.get_yticklabels()]
        labels[0]='0'
        cb1.ax.set_yticklabels(labels)


    if ax == ax35:
        cb1 = plt.colorbar(cs1,cax = cbaxes3,ticks=[0.0,0.03,0.06],format='%.2f',orientation='vertical')
        labels=[l.get_text() for l in cb1.ax.get_yticklabels()]
        labels[0]='0'
        cb1.ax.set_yticklabels(labels)

    if ax != ax41 and ax != ax42:
        ax.set_xticklabels([])
        ax.set_xlabel('')
    if ax != ax11 and ax != ax21 and ax != ax31 and ax != ax41:
        ax.set_yticklabels([])
        ax.set_ylabel('')

####################################################################################

def loc_plot(ax,r,z,loc):
    #   do the interpolation with cubic method
    ri = np.linspace(r.min(), r.max(), N)
    zi = np.linspace(z.min(), z.max(), N)
    loci = scipy.interpolate.griddata((r, z), loc, (ri[None,:], zi[:,None]), method='linear')

    ax.set_xlim((-13,13))
    ax.set_ylim((-19,19))

    minorLocator = MultipleLocator(5)
    majorLocator = MultipleLocator(10)
    ax.yaxis.set_minor_locator(minorLocator)
    ax.yaxis.set_major_locator(majorLocator)
    
    ax.xaxis.set_minor_locator(minorLocator)
    ax.xaxis.set_major_locator(majorLocator)
#    ax.xaxis.set_ticks(np.arange(-5, 6, 5))
    
    for ticks in ax.xaxis.get_ticklines() + ax.yaxis.get_ticklines(minor=True) + ax.yaxis.get_ticklines(minor=False):
        ticks.set_color('k')
    for pos in ['top', 'bottom', 'right', 'left']:
        ax.spines[pos].set_edgecolor('k')

    cs3 = ax.contourf(ri,zi,loci,500,cmap=maplinear)#YlGnBu
    #cs4 = ax.contour(ri,zi,loci,5,colors='0.75',hold='on')
    if ax == ax14:
        cb1 = plt.colorbar(cs3,cax = cbaxes1,ticks=[0.0,0.3,0.6,0.90],format='%.2f',orientation='vertical')
        labels=[l.get_text() for l in cb1.ax.get_yticklabels()]
        labels[0]='0'
        cb1.ax.set_yticklabels(labels)
    if ax == ax24:
        cb1 = plt.colorbar(cs3,cax = cbaxes2,ticks=[0.0,0.3,0.6,0.90],format='%.2f',orientation='vertical')
        labels=[l.get_text() for l in cb1.ax.get_yticklabels()]
        labels[0]='0'
        cb1.ax.set_yticklabels(labels)
    if ax == ax34:
        cb1 = plt.colorbar(cs3,cax = cbaxes3,ticks=[0.0,0.3,0.6,0.90],format='%.2f',orientation='vertical')
        labels=[l.get_text() for l in cb1.ax.get_yticklabels()]
        labels[0]='0'
        cb1.ax.set_yticklabels(labels)
    if ax == ax44:
        cb1 = plt.colorbar(cs3,cax = cbaxes4,ticks=[0.0,0.3,0.6,0.90],format='%.2f',orientation='vertical')
        labels=[l.get_text() for l in cb1.ax.get_yticklabels()]
        labels[0]='0'
        cb1.ax.set_yticklabels(labels)

    if ax != ax41 and ax != ax42 and ax != ax43 and ax != ax44:
        ax.set_xticklabels([])
        ax.set_xlabel('')
    if ax != ax11 and ax != ax21 and ax != ax31 and ax != ax41:
        ax.set_yticklabels([])
        ax.set_ylabel('')

####################################################################################
fig = plt.figure(figsize = (8,11) , dpi = 1000)

ax11 = plt.subplot(4,4,1)
ax12 = plt.subplot(4,4,2)
ax13 = plt.subplot(4,4,3)
ax14 = plt.subplot(4,4,4)

ax21 = plt.subplot(4,4,5)
ax22 = plt.subplot(4,4,6)
ax23 = plt.subplot(4,4,7)
ax24 = plt.subplot(4,4,8)

ax31 = plt.subplot(4,4,9)
ax32 = plt.subplot(4,4,10)
ax33 = plt.subplot(4,4,11)
ax34 = plt.subplot(4,4,12)

ax41 = plt.subplot(4,4,13)
ax42 = plt.subplot(4,4,14)
ax43 = plt.subplot(4,4,15)
ax44 = plt.subplot(4,4,16)

fig.subplots_adjust(wspace=0.05, hspace=0.05)

pos1 = ax14.get_position()
pos2 = ax24.get_position()
pos3 = ax34.get_position()
pos4 = ax44.get_position()

cbaxes1 = fig.add_axes([pos1.x0+pos1.width+0.01, pos1.y0, 0.02, pos1.height])
cbaxes2 = fig.add_axes([pos2.x0+pos2.width+0.01, pos2.y0, 0.02, pos2.height])
cbaxes3 = fig.add_axes([pos3.x0+pos3.width+0.01, pos3.y0, 0.02, pos3.height])
cbaxes4 = fig.add_axes([pos4.x0+pos4.width+0.01, pos4.y0, 0.02, pos4.height])

####################################################################################
#energy_plot(ax1)
loc_plot(ax11,x1n,z1n,neu_up1)
loc_plot(ax12,x2n,z2n,neu_up2)
loc_plot(ax13,x3n,z3n,neu_up3)
loc_plot(ax14,x4n,z4n,neu_up4)

loc_plot(ax21,x1n,z1n,neu_dw1)
loc_plot(ax22,x2n,z2n,neu_dw2)
loc_plot(ax23,x3n,z3n,neu_dw3)
loc_plot(ax24,x4n,z4n,neu_dw4)

loc_plot(ax31,x1p,z1p,pro_up1)
loc_plot(ax32,x2p,z2p,pro_up2)
loc_plot(ax33,x3p,z3p,pro_up3)
loc_plot(ax34,x4p,z4p,pro_up4)

loc_plot(ax41,x1p,z1p,pro_dw1)
loc_plot(ax42,x2p,z2p,pro_dw2)
loc_plot(ax43,x3p,z3p,pro_dw3)
loc_plot(ax44,x4p,z4p,pro_dw4)

####################################################################################

matplotlib.rc ('text', usetex=True)

fig.text(0.5, 0.04, r'x (fm)', ha='center')
fig.text(0.03, 0.5, r'z (fm)', va='center', rotation='vertical')

ax11.text(-11,21,r'$q_{20}=61  \mathrm{ b}$',color='black',fontsize=fontsize)
ax12.text(-11,21,r'$q_{20}=149 \mathrm{ b}$',color='black',fontsize=fontsize)
ax13.text(-11,21,r'$q_{20}=229 \mathrm{ b}$',color='black',fontsize=fontsize)
ax14.text(-11,21,r'$q_{20}=249 \mathrm{ b}$',color='black',fontsize=fontsize)

ax11.text(-11,13,r'$\mathcal{C}_{\mathrm{n,symm}}$',color='black',fontsize=fontsize)
ax21.text(-11,13,r'$\mathcal{C}_{\mathrm{n,asymm}}$',color='black',fontsize=fontsize)
ax31.text(-11,13,r'$\mathcal{C}_{\mathrm{p,symm}}$',color='black',fontsize=fontsize)
ax41.text(-11,13,r'$\mathcal{C}_{\mathrm{p,asymm}}$',color='black',fontsize=fontsize)

plt.savefig('pt178-localization-xz.ps')
#plt.show()
