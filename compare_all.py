# This takes yields from each of 4 different conditions:
#    - No dissipation, constant inertia
#    - No dissipation, original inertia
#    - Dissipation, constant inertia
#    - Dissipation, original inertia
# and plots the corresponding mass and charge yields, a la Fig 4 of PRC 93, 011304(R) (2016)
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib.ticker import MultipleLocator
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib.patches import Rectangle
import matplotlib
matplotlib.rc ('font',**{'family':'serif','serif':['Times New Roman']})
#matplotlib.rc ('text', usetex=True)


# Specify different functionals
infile0 = 'distro.out-UNEDF1-HFB'
infile1 = 'distro.out-SkMstar'
infile2 = 'distro.out-D1S'
# Specify different inertias
infile3 = 'distro.out-GCMp'
infile4 = 'distro.out-ATDHFp'
infile5 = 'distro.out-diss_constM'
# Specify different dissipations
infile6 = 'distro.out-05eta'
infile7 = 'distro.out-2eta'
infile8 = 'distro.out-0eta'
sigmaA = 6
sigmaZ = 4
outfile = 'compare_all.eps'

##########################################################################
def convolute_data(infile):
    ''' Reads a distro.out type file and performs a 2D Gaussian convolution'''
    data = np.genfromtxt(infile)
    A = data[:,0]
    Z = data[:,1]
    prob = data[:,2]

    
    prob_a = np.zeros(np.size(frag_a))
    dico_a = dict(zip(frag_a,prob_a))
    dico_a_conv = dict(zip(frag_a,prob_a))
    prob_z = np.zeros(np.size(frag_z))
    dico_z = dict(zip(frag_z,prob_z))
    dico_z_conv = dict(zip(frag_z,prob_z))
    
    prob_az = np.zeros(len(frag_a)*len(frag_z))
    a_grid, z_grid = np.meshgrid(frag_a,frag_z)
    a_grid = np.reshape(a_grid,(np.size(a_grid),1))
    z_grid = np.reshape(z_grid,(np.size(z_grid),1))
    
    frags = zip(a_grid.ravel(),z_grid.ravel())
    
    dico_az = dict(zip(frags,prob_az))
    dico_az_conv = dict(zip(frags,prob_az))
    
    for a,z,p in zip(A,Z,prob):
        if round(a) in frag_a and round(z) in frag_z:
            dico_a[int(round(a))] += p
            dico_z[int(round(z))] += p

    avals = gaussian_filter1d(dico_a.values(),sigmaA)
    zvals = gaussian_filter1d(dico_z.values(),sigmaZ)
    
    sum_a = sum(avals)
    sum_z = sum(zvals)

    return avals/sum_a, zvals/sum_z
##########################################################################
def preconvoluted(infile):
    A, Acoarse, Asmooth, Z, Zcoarse, Zsmooth = [], [], [], [], [], []
    # get data
    with open(infile) as input_data:
        # Skips text before the beginning of the interesting block:
        for line in input_data:
            if line.strip() == 'mass---initial % yield----% yield after smoothening':  # Or whatever test is needed
                break
        # Reads text until the end of the block:
        for line in input_data:  # This keeps reading the file
            if line.strip() == 'value of sigma for Z-distribution =    {}.0000000000000000'.format(sigmaZ):
                break
            floats = [float(x) for x in line.split()]
            A.append(floats[0])
            Acoarse.append(floats[1])
            Asmooth.append(floats[2])
    with open(infile) as input_data:
        # Skips text before the beginning of the interesting block:
        for line in input_data:
            if line.strip() == 'Z---initial % yield----% yield after smoothening':  # Or whatever test is needed
                break
        # Reads text until the end of the block:
        for line in input_data:
            floats = [float(x) for x in line.split()]
            Z.append(floats[0])
            Zcoarse.append(floats[1])
            Zsmooth.append(floats[2])
        sum_a = sum(Asmooth)
        sum_z = sum(Zsmooth)
    return A, np.array(Asmooth)/sum_a, Z, np.array(Zsmooth)/sum_z
##########################################################################
def yield_plot(ax,x,y,**sty):

    ax.set_ylim((0.0004,.11))

    # If you want the full distribution use this
#    minorLocator = MultipleLocator(round((max(x)-min(x))/6,-1))
#    majorLocator = MultipleLocator(round((max(x)-min(x))/3,-1))

    # If you want to zoom in on the interesting part of the distribution use this instead
    if ax == ax11 or ax == ax21 or ax == ax31:
#        ax.set_xlim((190,250))
        ax.set_xlim((147,245))
        minorLocator = MultipleLocator(5)
        majorLocator = MultipleLocator(10)
#        ax.set_xlim((min(x)+40,max(x)-20))
#        minorLocator = MultipleLocator(round(((max(x)-20)-(min(x)+40))/6,-1))
#        majorLocator = MultipleLocator(round(((max(x)-20)-(min(x)+40))/3,-1))
    elif ax == ax12 or ax == ax22 or ax == ax32:
#        ax.set_xlim((73,105))
        ax.set_xlim((59,102))
        ax12minorLocator = MultipleLocator(5)
        ax12majorLocator = MultipleLocator(10)
#        ax.set_xlim((min(x)+10,max(x)-15))
#        minorLocator = MultipleLocator(round(((max(x)-15)-(min(x)+10))/4,-1))
#        majorLocator = MultipleLocator(round(((max(x)-15)-(min(x)+10))/2,-1))

    # Switches the y-axis scale to the right for plots on the right
    if ax == ax12 or ax == ax22 or ax == ax32:
        ax.yaxis.tick_right()
    ax.yaxis.set_ticks_position('both')

    ax.tick_params(which='both',direction='in')

    myfig = ax.semilogy(x, y, **sty)
    return myfig
##########################################################################

frag_a = np.arange(147,295)
frag_z = np.arange(59,119)

A0smooth, Z0smooth = convolute_data(infile0)
A1smooth, Z1smooth = convolute_data(infile1)
frag_a2, A2smooth, frag_z2, Z2smooth = preconvoluted(infile2)
A3smooth, Z3smooth = convolute_data(infile3)
A4smooth, Z4smooth = convolute_data(infile4)
A5smooth, Z5smooth = convolute_data(infile5)
A6smooth, Z6smooth = convolute_data(infile6)
A7smooth, Z7smooth = convolute_data(infile7)
A8smooth, Z8smooth = convolute_data(infile8)

fig = plt.figure(figsize = (5.0,6.5) , dpi = 500)

ax11 = plt.subplot(3,2,1)
ax12 = plt.subplot(3,2,2)
ax21 = plt.subplot(3,2,3)
ax22 = plt.subplot(3,2,4)
ax31 = plt.subplot(3,2,5)
ax32 = plt.subplot(3,2,6)

fig.subplots_adjust(wspace=0.00, hspace=0.00)

# Different functionals (HFB1, SkM*, D1S)
fig111, = yield_plot(ax11,frag_a, A0smooth,linestyle='-', color='k')
fig121, = yield_plot(ax12,frag_z, Z0smooth,linestyle='-', color='k')

fig112, = yield_plot(ax11,frag_a, A1smooth,linestyle='-', color='xkcd:dark orange')
fig122, = yield_plot(ax12,frag_z, Z1smooth,linestyle='-', color='xkcd:dark orange')

fig113, = yield_plot(ax11,frag_a2,A2smooth,linestyle='-', color='c')
fig123, = yield_plot(ax12,frag_z2,Z2smooth,linestyle='-', color='c')

# Different inertias (ATDHFBnp, GCMp, ATDHFBp', Constant M)
fig211, = yield_plot(ax21,frag_a, A0smooth,linestyle='-', color='k')
fig221, = yield_plot(ax22,frag_z, Z0smooth,linestyle='-', color='k')

fig212, = yield_plot(ax21,frag_a, A3smooth,linestyle=':', color='k')
fig222, = yield_plot(ax22,frag_z, Z3smooth,linestyle=':', color='k')

fig213, = yield_plot(ax21,frag_a, A4smooth,linestyle='--', color='k')
fig223, = yield_plot(ax22,frag_z, Z4smooth,linestyle='--', color='k')

fig214, = yield_plot(ax21,frag_a, A5smooth,linestyle='-.', color='k')
fig224, = yield_plot(ax22,frag_z, Z5smooth,linestyle='-.', color='k')

# Different dissipations (eta, 1/2*eta, 2*eta, 0*eta)
fig311, = yield_plot(ax31,frag_a, A0smooth,linestyle='-', color='k')
fig321, = yield_plot(ax32,frag_z, Z0smooth,linestyle='-', color='k')

fig312, = yield_plot(ax31,frag_a, A6smooth,linestyle='-', color='xkcd:medium grey')
fig322, = yield_plot(ax32,frag_z, Z6smooth,linestyle='-', color='xkcd:medium grey')

fig313, = yield_plot(ax31,frag_a, A7smooth,linestyle='-', color='xkcd:dark grey')
fig323, = yield_plot(ax32,frag_z, Z7smooth,linestyle='-', color='xkcd:dark grey')

fig314, = yield_plot(ax31,frag_a, A8smooth,linestyle='-', color='xkcd:cement')
fig324, = yield_plot(ax32,frag_z, Z8smooth,linestyle='-', color='xkcd:cement')
ax31.fill_between(frag_a, A6smooth, A8smooth, color='xkcd:light grey')
ax32.fill_between(frag_z, Z6smooth, Z8smooth, color='xkcd:light grey')

font_size=18
axis_dico = {'fontsize':font_size}

ax31.set_xlabel('Mass',fontsize=font_size)
ax32.set_xlabel('Charge',fontsize=font_size)

ax21.set_ylabel('% yield',fontsize=font_size)

# Labels to describe each set of plots
ax12.set_ylabel('functional', fontsize=font_size, color='xkcd:grey')
ax22.set_ylabel('inertia',    fontsize=font_size, color='xkcd:grey')
ax32.set_ylabel('dissipation',fontsize=font_size, color='xkcd:grey')

# Blank entry which allows us to cheat and create blank entries in legend
extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
# Figure legend
lgd = ax31.legend((extra,fig121,fig122,fig123,extra, \
            extra,fig221,fig222,fig223,fig224, \
            extra,fig321,fig323,fig322,fig324),\
          (r'$Top$',r'UNEDF1$_{HFB}$',r'SkM$^*$',r'D1S', '',\
           r'$Middle$',r'ATDHFB$_{np}$',r'GCM$_p$',r'ATDHFB$_p$',r'Constant $\mathcal{M}$',\
           r'$Bottom$',r'$\eta_0$',r'$2\eta_0$',r'$\frac{1}{2}\eta_0$',r'No dissipation'),\
           ncol=3, loc='lower center', bbox_to_anchor=(1.0,-1.35), fontsize=font_size-4)

## Hide the first and last values on the x-axis to keep adjacent plots from overlapping
#xticks = ax11.xaxis.get_major_ticks()
#xticks[0].label1.set_visible(False)
#xticks[-1].label1.set_visible(False)
#xticks = ax12.xaxis.get_major_ticks()
#xticks[0].label1.set_visible(False)
#xticks[-1].label1.set_visible(False)

# x-labels
ax31_xlabels = (150,175,200,225)
ax11.set_xticks(ax31_xlabels)
ax11.set_xticklabels('',fontdict=axis_dico)
ax21.set_xticks(ax31_xlabels)
ax21.set_xticklabels('',fontdict=axis_dico)
ax31.set_xticks(ax31_xlabels)
ax31.set_xticklabels(ax31_xlabels,fontdict=axis_dico)

ax32_xlabels = (65,75,85,95)
ax12.set_xticks(ax32_xlabels)
ax12.set_xticklabels('',fontdict=axis_dico)
ax22.set_xticks(ax32_xlabels)
ax22.set_xticklabels('',fontdict=axis_dico)
ax32.set_xticks(ax32_xlabels)
ax32.set_xticklabels(ax32_xlabels,fontdict=axis_dico)

# y-labels
ax11.set_yticklabels(('','',0.1,1,10),fontdict=axis_dico)
ax12.set_yticklabels(('','',0.1,1,10),fontdict=axis_dico)
ax21.set_yticklabels(('','',0.1,1,10),fontdict=axis_dico)
ax22.set_yticklabels(('','',0.1,1,10),fontdict=axis_dico)
ax31.set_yticklabels(('','',0.1,1,10),fontdict=axis_dico)
ax32.set_yticklabels(('','',0.1,1,10),fontdict=axis_dico)

ax12.yaxis.set_label_position("right")
ax22.yaxis.set_label_position("right")
ax32.yaxis.set_label_position("right")

# Lines to guide the eye to 208Pb
ax11.vlines(x=208, ymin=0.009, ymax=0.1, color='k', linewidth=0.5)
ax12.vlines(x= 82, ymin=0.009, ymax=0.1, color='k', linewidth=0.5)
ax21.vlines(x=208, ymin=0.009, ymax=0.1, color='k', linewidth=0.5)
ax22.vlines(x= 82, ymin=0.009, ymax=0.1, color='k', linewidth=0.5)
ax31.vlines(x=208, ymin=0.009, ymax=0.1, color='k', linewidth=0.5)
ax32.vlines(x= 82, ymin=0.009, ymax=0.1, color='k', linewidth=0.5)

# Figure title
ttl = fig.suptitle(r'$^{294}$Og Heavy Fragment',y=0.95,color='black',fontsize=20,backgroundcolor='w')

plt.savefig(outfile,  bbox_inches='tight', bbox_extra_artists=(lgd,ttl,),)
