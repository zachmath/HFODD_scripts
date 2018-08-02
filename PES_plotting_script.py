#!/usr/bin/python

## for LaTeX in the .ps
import matplotlib
matplotlib.use ("PS")
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

np.set_printoptions(threshold=np.nan) # DON'T KEEP THIS FOR LONG!!! IT'LL GET REALLY ANNOYING!!!


#################################
#### This section contains the interactive portion of the program
####  where the user decides which input and output files to use
#################################


lvlcross = raw_input("\n\n Do you have a level crossing and between fission and fusion configurations? \n")

if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    infilefission = raw_input("\n Please list the name of the input file corresponding to the fission configuration: \n")
    cutofffission = input("\n Please type the z-axis cutoff scale for the fission configuration: \n")
    infilefusion = raw_input("\n Please list the name of the input file corresponding to the fusion configuration: \n")
#    cutofffusion = input("\n Please type the energy cutoff scale for the fusion configuration: \n")
else:
    infilefission = raw_input("\n Please list the name of the input file: \n")
    cutofffission = input("\n Please type the z-axis cutoff scale: \n")
    # What to do below? Because you've got everything down there written for two datasets, but here you only have one! Do you just input a second dummy dataset here? Or do you hide any references to the second dataset inside an "if lvlcross=yes" loop?


xaxis = raw_input("\n Which multipole moment would you like to plot on the x-axis? (Q20 [default], Q22, Q30) \n")
if xaxis in ['Q20', 'q20', 'q_20', 'Q_20']:
    xaxis="Q20"
    xlabel=r"$ Q_{20} \, (\rm{b}) $"
#    xlabel=r"Elongation $\, (\rm{b}) $"
    xcol=0
elif xaxis in ['Q22', 'q22', 'q_22', 'Q_22']:
    xaxis="Q22"
    xlabel=r"$ Q_{22} \, (\rm{b}) $"
#    xlabel=r"Triaxiality $\, (\rm{b}) $"
    xcol=2
elif xaxis in ['Q30', 'q30', 'q_30', 'Q_30']:
    xaxis="Q30"
    xlabel=r"$ Q_{30} \, (\rm{b}^\frac{3}{2}) $"
#    xlabel=r"Mass Asymmetry $\, (\rm{b}^\frac{3}{2}) $"
    xcol=1
elif xaxis in ['Q40', 'q40', 'q_40', 'Q_40']:
    xaxis="Q40"
    xlabel=r"Neck $\, (\rm{b}^2) $"
    xcol=3
elif xaxis in ['Q50', 'q50', 'q_50', 'Q_50']:
    xaxis="Q50"
    xlabel=r"$ Q_{50} \, (\rm{b}^\frac{5}{2}) $"
    xcol=4
elif xaxis in ['Q60', 'q60', 'q_60', 'Q_60']:
    xaxis="Q60"
    xlabel=r"$ Q_{60} \, (\rm{b}^3) $"
    xcol=5
elif xaxis in ['Q70', 'q70', 'q_70', 'Q_70']:
    xaxis="Q70"
    xlabel=r"$ Q_{70} \, (\rm{b}^\frac{7}{2}) $"
    xcol=6
elif xaxis in ['Q80', 'q80', 'q_80', 'Q_80']:
    xaxis="Q80"
    xlabel=r"$ Q_{80} \, (\rm{b}^4) $"
    xcol=7
else:
    xaxis="Q20"
    xlabel=r"$ Q_{20} \, (\rm{b}) $"
#    xlabel=r"Elongation $\, (\rm{b}) $"
    xcol=0
print "\n The x-axis will show %s, %s " %(xaxis, xlabel)

yaxis = raw_input("\n Which multipole moment would you like to plot on the y-axis? (Q20, Q22, Q30 [default]) \n")
if yaxis in ['Q20', 'q20', 'q_20', 'Q_20']:
    yaxis="Q20"
    ylabel=r"$ Q_{20} \, (\rm{b}) $"
#    ylabel=r"Elongation $\, (\rm{b}) $"
    ycol=0
elif yaxis in ['Q22', 'q22', 'q_22', 'Q_22']:
    yaxis="Q22"
    ylabel=r"$ Q_{22} \, (\rm{b}) $"
#    ylabel=r"Triaxiality $\, (\rm{b}) $"
    ycol=2
elif yaxis in ['Q30', 'q30', 'q_30', 'Q_30']:
    yaxis="Q30"
    ylabel=r"$ Q_{30} \, (\rm{b}^\frac{3}{2}) $"
#    ylabel=r"Mass Asymmetry $\, (\rm{b}^\frac{3}{2}) $"
    ycol=1
elif yaxis in ['Q40', 'q40', 'q_40', 'Q_40']:
    yaxis="Q40"
    ylabel=r"Neck $\, (\rm{b}^2) $"
    ycol=3
elif yaxis in ['Q50', 'q50', 'q_50', 'Q_50']:
    yaxis="Q50"
    ylabel=r"$ Q_{50} \, (\rm{b}^\frac{5}{2}) $"
    ycol=4
elif yaxis in ['Q60', 'q60', 'q_60', 'Q_60']:
    yaxis="Q60"
    ylabel=r"$ Q_{60} \, (\rm{b}^3) $"
    ycol=5
elif yaxis in ['Q70', 'q70', 'q_70', 'Q_70']:
    yaxis="Q70"
    ylabel=r"$ Q_{70} \, (\rm{b}^\frac{7}{2}) $"
    ycol=6
elif yaxis in ['Q80', 'q80', 'q_80', 'Q_80']:
    yaxis="Q80"
    ylabel=r"$ Q_{80} \, (\rm{b}^4) $"
    ycol=7
else:
    yaxis="Q30"
    ylabel=r"$ Q_{30} \, (\rm{b}^\frac{3}{2}) $"
#    ylabel=r"Mass Asymmetry $\, (\rm{b}^\frac{3}{2}) $"
    ycol=1
print "\n The y-axis will show %s, %s" %(yaxis, ylabel)


zaxis = raw_input("\n What would you like to plot on the z-axis? (Energy [default], neck (qN), Q20, Q22, Q30) \n")
if zaxis in ['Q20', 'q20', 'q_20', 'Q_20']:
    zaxis="Q20"
    zlabel=r"$ Q_{20} \, (\rm{b}) $"
#    zlabel=r"Elongation $\, (\rm{b}) $"
    zcol=0
elif zaxis in ['Q22', 'q22', 'q_22', 'Q_22']:
    zaxis="Q22"
    zlabel=r"$ Q_{22} \, (\rm{b}) $"
#    zlabel=r"Triaxiality $\, (\rm{b}) $"
    zcol=2
elif zaxis in ['Q30', 'q30', 'q_30', 'Q_30']:
    zaxis="Q30"
    zlabel=r"$ Q_{30} \, (\rm{b}^\frac{3}{2}) $"
#    zlabel=r"Mass Asymmetry $\, (\rm{b}^\frac{3}{2}) $"
    zcol=1
elif zaxis in ['Q40', 'q40', 'q_40', 'Q_40']:
    zaxis="Q40"
    zlabel=r"Neck $\, (\rm{b}^2) $"
    zcol=3
elif zaxis in ['Q50', 'q50', 'q_50', 'Q_50']:
    zaxis="Q50"
    zlabel=r"$ Q_{50} \, (\rm{b}^\frac{5}{2}) $"
    zcol=4
elif zaxis in ['Q60', 'q60', 'q_60', 'Q_60']:
    zaxis="Q60"
    zlabel=r"$ Q_{60} \, (\rm{b}^3) $"
    zcol=5
elif zaxis in ['Q70', 'q70', 'q_70', 'Q_70']:
    zaxis="Q70"
    zlabel=r"$ Q_{70} \, (\rm{b}^\frac{7}{2}) $"
    zcol=6
elif zaxis in ['Q80', 'q80', 'q_80', 'Q_80']:
    zaxis="Q80"
    zlabel=r"$ Q_{80} \, (\rm{b}^4) $"
    zcol=7
elif zaxis in ['neck', 'qn', 'QN', 'qN']:
    zaxis="qN"
    zlabel=r"Neck $\, (\rm{Q_N}) $"
    zcol=11
elif zaxis in ['deltaN', 'deltan', 'Deltan', 'DeltaN']:
    zaxis="deltaN"
    zlabel=r"$10\Delta_N\, (\rm{MeV}) $"
    zcol=12
elif zaxis in ['deltaP', 'deltap', 'Deltap', 'DeltaP']:
    zaxis="deltaP"
    zlabel=r"$10\Delta_P\, (\rm{MeV}) $"
    zcol=13
elif zaxis in ['epairN', 'epairn', 'Epairn', 'EpairN']:
    zaxis="EpairN"
    zlabel=r"$E_{pair}^N\, (\rm{MeV}) $"
    zcol=14
elif zaxis in ['epairP', 'epairp', 'Epairp', 'EpairP']:
    zaxis="EpairP"
    zlabel=r"$E_{pair}^P\, (\rm{MeV}) $"
    zcol=15
elif zaxis in ['zneck', 'zn', 'ZN', 'zN']:
    zaxis="zN"
    zlabel=r"Protons in Neck $\, (\rm{Z_N}) $"
    zcol=16
elif zaxis in ['Z1', 'z1']:
    zaxis="Z1"
    zlabel="Charge of fragment 1"
    zcol=17
elif zaxis in ['A1', 'a1']:
    zaxis="A1"
    zlabel="Mass of fragment 1"
    zcol=18
else:
    zaxis="Energy"
    zlabel=r"Energy $\, (\rm{MeV}) $"
    zcol=10
print "\n The z-axis will show %s, %s" %(zaxis, zlabel)

dots = raw_input("\n Would you like to draw a dot at every single point from the original data set? This lets you see visually which grid points converged and which ones didn't. \n")

pathway = raw_input("\n Would you like to superimpose a fission pathway onto the PES? \n")
if pathway in ['y', 'Y', 'yes', 'Yes', 'YES']:
    pathfile = raw_input("\n Please list the name of the input file which contains the fission pathway data: \n")


description = raw_input("\n Would you like to include some description text in the top left corner? \n")
if description in ['y', 'Y', 'yes', 'Yes', 'YES']:
    desctext = raw_input("Please enter your text below: (eg '$^{176}$Pt \\n UNEDF1') \n")

outname = raw_input("\n Please provide a name for the output .eps file [default name 'output']: \n")
if outname=='':
    outname="output"
outfile = "%s.eps" % outname
print "\n The plot will be output to %s. \n" % outfile




#################################
##### Import the data
#################################


data = np.genfromtxt (infilefission, skip_header=1)
x0 = data[:,xcol]
y0 = data[:,ycol]
z0 = data[:,zcol]
#z0 = data[:,10]

if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    data = np.genfromtxt (infilefusion, skip_header=1)
    x1 = data[:,xcol]
    y1 = data[:,ycol]
    z1 = data[:,zcol]
#    z1 = data[:,10]

if pathway in ['y', 'Y', 'yes', 'Yes', 'YES']:
    data = np.genfromtxt (pathfile)
    x2 = data[:,xcol]
    y2 = data[:,ycol]
#    z2 = data[:,2]

if zaxis in ['deltaN', 'deltan', 'Deltan', 'DeltaN', 'deltaP', 'deltap', 'Deltap', 'DeltaP']:
    z0 = 10.0*z0

## Uncomment these lines if you only want to look at a small section of the PES
#x0max = 175
#xyz0 = zip(x0,y0,z0)
#xyz0 = [xyz for xyz in xyz0 if xyz[0]<x0max]
#y0max = 50
#xyz0 = [xyz for xyz in xyz0 if xyz[1]<y0max]
#x0min = 0
#xyz0 = [xyz for xyz in xyz0 if xyz[0]>x0min]
#
#x0 = [item[0] for item in xyz0]
#y0 = [item[1] for item in xyz0]
#z0 = [item[2] for item in xyz0]

#################################
##### Adjust your energy scale to set E=0 at or around Q20=Q30=0
#################################


# Set your origin E=0 to the point in your fission configuration with the minimum energy (hopefully it should be right around Q20=Q30=0)
min_z0 = -2080.263986 #z0.min() #0 #
z0 = [z - min_z0 for z in z0]
#z0 = z0-min_z0
if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    z1 = [z - min_z0 for z in z1]

### Cut out those points which are just skewing the entire graph
##index = np.arange(len(z0))
##for i in index:
##    zval = z0[i]
##    if zval > (z0.min ()+cutofffission):
##        z0[i]=z0.min ()+cutofffission 

##if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
##    index = np.arange(len(z1))
##    for i in index:
##        zval = z1[i]
##        if zval > (z0.min ()+cutofffission):
##            z1[i]=z0.min ()+cutofffission 


#################################
##### Interpolate your data to fill in holes and give you a nice, smooth contour
#################################


# basis grid for the interpolation
#xi = x0
#yi = y0
xi = np.linspace (min (x0) , max (x0), num=200)
yi = np.linspace (min (y0) , max (y0), num=200)
#xi = np.linspace (0.0 , 175.0)
#yi = np.linspace (-2.0 , 30.0)

# interpolate data
X0, Y0 = np.meshgrid (xi , yi)
Z0 = griddata(x0 , y0 , z0 , xi , yi, interp='nn')

if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    Z1 = griddata(x1 , y1 , z1 , xi , yi, interp='nn')


#################################
##### Pick out the lower energy configuration at each point (i.e. fission vs fusion configuration; irrelevant if you don't have a level crossing)
#################################


if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    Zplot = np.fmin(Z0,Z1)
else:
    Zplot = Z0

Zplot[Zplot >= cutofffission-1.5] = np.nan             # Not sure about these two lines just yet
#Zplot[Zplot <= -20] = -20 #np.nan
Zplot[Zplot <= -2] = -2 #np.nan

maxZplot = np.nanmax (Zplot);
minZplot = np.nanmin (Zplot);


#################################
##### Plot the data
#################################


# APS required dpi, figsize can change
#fig = plt.figure (figsize = (8.0 , 3.0) , dpi = 1200)
fig = plt.figure (figsize = (14 , 7) , dpi = 1200)

# add a plot on the figure
ax = fig.add_subplot (111)

# set labels
ax.set_xlabel (xlabel , fontsize=30)
ax.set_ylabel (ylabel , fontsize=30)

# set ticks (min, max, step) gives: [min , min+step , ... , max-step]
tab_range = np.arange (0.0, X0.max(), 50.0)
#tab_range = np.arange (0.0, 300.0, 100.0)
ax.xaxis.set_ticks (tab_range)

tab_range = np.arange (0.0, Y0.max(), 10.0)
#tab_range = np.arange (0.0, 35.0, 10.0)
ax.yaxis.set_ticks (tab_range)

origin = 'lower'

# This gives you your attractive color gradient contour
CS0 = plt.contourf (X0 , Y0 , Zplot , 25 , origin=origin , vmin=minZplot , vmax=maxZplot, cmap=plt.cm.jet)

# This overlays nice 'altitude' labels on top of your contour plot (Behind the scenes, what it's really doing is drawing and labelling individual contour lines, but you can't see them since they're the same color as the gradient)
CS1 = plt.contour (X0 , Y0 , Zplot , 5 , origin=origin , vmin=minZplot , vmax=maxZplot, cmap=plt.cm.jet)
plt.clabel(CS1, inline=1, fontsize=20, colors='k')

# This draws a dot at every single point from the original data set, before they are used to make the interpolated contour. It lets you see visually which grid points converged and which ones didn't.
if dots in ['n', 'N', 'no', 'No', 'NO']:
    pass
else:
    CS2 = plt.scatter (x0 , y0 , c=z0 , vmin=minZplot , vmax=maxZplot, cmap=plt.cm.jet)
#    plot (x0, y0, 'k.')
    if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
        plot (x1, y1, 'g.')

# This plots the fission pathway
if pathway in ['y', 'Y', 'yes', 'Yes', 'YES']:
    plot (x2 , y2, color='blue')



#################################
##### Add some text to the plot
#################################


if description in ['y', 'Y', 'yes', 'Yes', 'YES']:
    text(0.2, 0.9, desctext,
        horizontalalignment='center',
        verticalalignment='center',
        transform = ax.transAxes)



#################################
##### Color bar
#################################


# compress the figure to make some room for the colorbar
fig.subplots_adjust (right=0.88)

# set the colorbar position and size
# [distance to the z axis , height from the bottom , width of the bar , length of the bar]
cbar_ax = fig.add_axes ([0.9 , 0.1 , 0.04 , 0.8])

# ticks along the colorbar
step = 5
decimal_number = 0#-1
v = np.linspace (0 , cutofffission, step , endpoint=True).tolist ()
#v = np.linspace (0 , cutofffission, step , endpoint=True).tolist ()
#v = np.linspace (round (minZplot , decimal_number) , round (maxZplot + (maxZplot-minZplot)/step , decimal_number) , step , endpoint=True).tolist ()
v = [round (elem , decimal_number) for elem in v] # warning, these are positions of ticks, the "round" function can lead to irregular spacings


# plot the colorbar
cb = plt.colorbar (CS0 , cax=cbar_ax , ticks=v , norm=matplotlib.colors.Normalize (vmin=minZplot , vmax=maxZplot))
cb.set_label(zlabel , fontsize=30, rotation=270, labelpad=20)
#cb.set_label(r"Energy $\, (\rm{MeV}) $" , fontsize=20, rotation=270, labelpad=20)

# to get scientific notation (conflict with APS font)
#matplotlib.rcParams['axes.unicode_minus'] = False
#cb.formatter.set_powerlimits ((0 , 0))
#cb.update_ticks ()


# hide the exponent generated by the scientific notation
# conflict with internal LaTeX routines
# look at the maxZplot which is printed at the execution, look at the colorbar ticks and deduce the exponent
# then add it in the label definition (APS recommended: "x (10^2 fm)")
cb.ax.get_yaxis ().get_offset_text ().set_visible (False)



#################################
##### Save the final result
#################################


# to call external LaTeX libraries for dealing with latex command not included in python
# will produce conflicts if called before
#matplotlib.rc ('text', usetex=True)


# to add some text on the graph
# not tested
#ax.text (9 , 0 , 0 , "toto" , color='red')
#ax.annotate(r"$ \boldsymbol{ {1/2}^{+} } $" , xy=(6.3 , 6.5) , color='white' , ha='center' , fontsize=23)


# save in ps format, cannot be donne directly in pdf and eps has no bounding box
# follow the instruction below to get a pdf with bounding box
fig.savefig (outfile) # NOTE: This won't work until you've defined "fig."
# in the terminal:
# ps2eps -f test.ps ; epstopdf test.eps


