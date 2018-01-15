from pylab import *
from matplotlib import rc, rcParams,gridspec
import matplotlib.colors as mcolors
from scipy import interpolate
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
import os
import glob
import profile

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

def getin(filename):
    #  Import the data from a text file and save as a 2D matrix.
    rho = genfromtxt('Rhon'+filename,comments='*')
    print('rho=',rho)
    rho[1:,:] = rho[1:,:] + genfromtxt('Rhop'+filename,comments='*')[1:,:]
    print('rho=',rho)
    loc = genfromtxt('Locn'+filename,comments='*')
    loc[1:,:] = sqrt(loc[1:,:] * genfromtxt('Locp'+filename,comments='*')[1:,:])
    # Interpolate it
    dx=rho[0,0]
    dy=rho[0,1]
    time=rho[0,2]
    nx=rho.shape[0]-1
    ny=rho.shape[1]
    x1=((nx-1)*dx)/2
    y1=((ny-1)*dy)/2
    x = np.arange(-x1, x1+dx/2, dx)
    y = np.arange(-y1, y1+dy/2, dy)
    print('dx,dy,time,nx,ny,x1,y1=',dx,dy,time,nx,ny,x1,y1)
#    rhoi = interpolate.interp2d(x, y, rho[1:,:], kind='cubic')
#    loci = interpolate.interp2d(x, y, loc[1:,:], kind='cubic')
    rhoi = interpolate.interp2d(x, y, rho[3], kind='cubic')
    loci = interpolate.interp2d(x, y, loc[3], kind='cubic')
    return (rhoi,loci,dx,dy,nx,ny,x,y,time)
    
def plot_data(ax,ext_x1,ext_x2,ext_y1,ext_y2,rhoi,loci,xnew,ynew,time,mask):
    X,Y=np.meshgrid(xnew,ynew)
    ax.set_xlim(ext_x1,ext_x2)
    ax.set_ylim(ext_y1,ext_y2)
    norm = mpl.colors.Normalize(vmin=0.0,vmax=1.0)
    plt.contour(X, Y, rhoi(xnew,ynew), levels=[0.05])
    if(mask):
        maxrho=rhoi(xnew,ynew).max()
        plt.imshow(loci(xnew, ynew)*rhoi(xnew,ynew)/maxrho, extent=[ext_x1,ext_x2,ext_y1,ext_y2], cmap=maplinear, interpolation='bilinear', norm=norm)
    else:
        plt.imshow(loci(xnew, ynew), extent=[ext_x1,ext_x2,ext_y1,ext_y2], cmap=maplinear, interpolation='bilinear', norm=norm)
    plt.xticks([],[])
    plt.yticks([],[])
    plt.text(0.02, 0.96,str(int(round(time))), va='top', ha='left',transform=ax.transAxes,color="k")
        
def txt2pdf_rholocevo6(filenames,mask=False):
    print(filenames)
    ext_x1=-12
    ext_x2=12
    ext_y1=-12
    ext_y2=12
    xnew = np.arange(ext_x1, ext_x2+0.05, 0.05)
    ynew = np.arange(ext_y1, ext_y2+0.05, 0.05)
    #generate plots
    fig = plt.figure(1,figsize=(6,9))
    gs = gridspec.GridSpec(4, 2,width_ratios=[1,1],height_ratios=[0.1, 1, 1, 1]) 
    gs.update(wspace=0.04, hspace=0.04, left=0.15 , right=0.95 , top=0.94 , bottom=0.09)
    
    ax1=plt.subplot(gs[1,0])
    rhoi,loci,dx,dy,nx,ny,x,y,time=getin(filenames[0])
    plot_data(ax1,ext_x1,ext_x2,ext_y1,ext_y2,rhoi,loci,xnew,ynew,time,mask)
    plt.yticks([-10,0,10],[-10,0,10])
    
    ax2=plt.subplot(gs[1,1])
    rhoi,loci,dx,dy,nx,ny,x,y,time=getin(filenames[1])
    plot_data(ax2,ext_x1,ext_x2,ext_y1,ext_y2,rhoi,loci,xnew,ynew,time,mask)
    
    ax3=plt.subplot(gs[2,0])
    rhoi,loci,dx,dy,nx,ny,x,y,time=getin(filenames[2])
    plot_data(ax3,ext_x1,ext_x2,ext_y1,ext_y2,rhoi,loci,xnew,ynew,time,mask)
    plt.yticks([-10,0,10],[-10,0,10])
    
    ax4=plt.subplot(gs[2,1])
    rhoi,loci,dx,dy,nx,ny,x,y,time=getin(filenames[3])
    plot_data(ax4,ext_x1,ext_x2,ext_y1,ext_y2,rhoi,loci,xnew,ynew,time,mask)
    ax4.axhline(y=-1.55, linewidth=.5, color="k")
    ax4.axhline(y=1.55, linewidth=.5, color="k")
    ax4.axhline(y=-6, linewidth=.5, color="k")
    ax4.axhline(y=6, linewidth=.5, color="k")
    plt.text(10, 3.55,r'$^{12}$C', va='center', ha='center',color="k")
    plt.text(10, -3.95,r'$^{12}$C', va='center', ha='center',color="k")
    
    ax5=plt.subplot(gs[3,0])
    rhoi,loci,dx,dy,nx,ny,x,y,time=getin(filenames[4])
    plot_data(ax5,ext_x1,ext_x2,ext_y1,ext_y2,rhoi,loci,xnew,ynew,time,mask)
    plt.xticks([-10,0,10],[-10,0,10])
    plt.yticks([-10,0,10],[-10,0,10])

    ax6=plt.subplot(gs[3,1])
    rhoi,loci,dx,dy,nx,ny,x,y,time=getin(filenames[5])
    plot_data(ax6,ext_x1,ext_x2,ext_y1,ext_y2,rhoi,loci,xnew,ynew,time,mask)
    plt.xticks([-10,0,10],[-10,0,10])
    ax6.axhline(y=0, linewidth=.5, color="k")
    ax6.axhline(y=-3.4, linewidth=.5, color="k")
    ax6.axhline(y=3.4, linewidth=.5, color="k")
    ax6.axhline(y=-6, linewidth=.5, color="k")
    ax6.axhline(y=6, linewidth=.5, color="k")
    plt.text(10, 4.7,r'$\alpha$', va='center', ha='center',color="k")
    plt.text(10, -4.7,r'$\alpha$', va='center', ha='center',color="k")
    plt.text(10, 1.5,r'$^{12}$C', va='center', ha='center',color="k")
    plt.text(10, -1.9,r'$^{12}$C', va='center', ha='center',color="k")
    
    cax=plt.subplot(gs[0,:])
    cbar = plt.colorbar(cax = cax, orientation='horizontal')
    cbar.solids.set_rasterized(True)
    cbar.ax.xaxis.set_ticks_position('top')
    cbar.ax.xaxis.set_label_position('top')
    
    fig.text(0.56,0.02,r"$x$ (fm)",va="center",ha="center")
    fig.text(0.02,0.5,r"$z$ (fm)",va="center",ha="center",rotation=90)
    
    if(mask):    
        plt.savefig("RhoLoc_evo6_mask.pdf", format='pdf', dpi=500)
    else:
        plt.savefig("RhoLoc_evo6.pdf", format='pdf', dpi=500)
        
    plt.close()

c = mcolors.ColorConverter().to_rgb
maplinear = make_colormap([c('white'),c('blue'),0.2, c('blue'), c('cyan'), 0.4, c('cyan'), c('green'), 0.6, c('green'), c('yellow'), 0.8, c('yellow'), c('red')])
rc('text',usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern'],'size':18})

txt2pdf_rholocevo6(['_000001.txt','_000002.txt','_000003.txt','_000004.txt','_00005.txt','_00006.txt'])

    
    
    
    
