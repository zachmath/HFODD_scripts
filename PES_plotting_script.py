#!/usr/bin/python

## for LaTeX in the .ps
import matplotlib
matplotlib.use ("PS")
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

np.set_printoptions(threshold=np.nan) # DON'T KEEP THIS FOR LONG!!! IT'LL GET REALLY ANNOYING!!!


#################################
#### This section contains the interactive portion of the program
####  where the user decides which input and output files to use
#################################


lvlcross = raw_input("\n\n Do you have a level crossing and between fission and fusion configurations? \n")

if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    infilefission = raw_input("\n Please list the name of the input file corresponding to the fission configuration: \n")
    cutofffission = input("\n Please type the energy cutoff scale for the fission configuration: \n")
    infilefusion = raw_input("\n Please list the name of the input file corresponding to the fusion configuration: \n")
#    cutofffusion = input("\n Please type the energy cutoff scale for the fusion configuration: \n")
else:
    infilefission = raw_input("\n Please list the name of the input file: \n")
    cutofffission = input("\n Please type the energy cutoff scale: \n")
    # What to do below? Because you've got everything down there written for two datasets, but here you only have one! Do you just input a second dummy dataset here? Or do you hide any references to the second dataset inside an "if lvlcross=yes" loop?


xaxis = raw_input("\n Which multipole moment would you like to plot on the x-axis? (Q20 [default], Q22, Q30) \n")
if xaxis in ['Q20', 'q20', 'q_20', 'Q_20']:
    xaxis="Q20"
    xlabel=r"Elongation $\, (\rm{b}) $"
    xcol=0
elif xaxis in ['Q22', 'q22', 'q_22', 'Q_22']:
    xaxis="Q22"
    xlabel=r"Triaxiality $\, (\rm{b}) $"
    xcol=1
elif xaxis in ['Q30', 'q30', 'q_30', 'Q_30']:
    xaxis="Q30"
    xlabel=r"Mass Asymmetry $\, (\rm{b}^\frac{3}{2}) $"
    xcol=2
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
    xlabel=r"Elongation $\, (\rm{b}) $"
    xcol=0
print "\n The x-axis will show %s, %s " %(xaxis, xlabel)

yaxis = raw_input("\n Which multipole moment would you like to plot on the y-axis? (Q20, Q22, Q30 [default]) \n")
if yaxis in ['Q20', 'q20', 'q_20', 'Q_20']:
    yaxis="Q20"
    ylabel=r"Elongation $\, (\rm{b}) $"
    ycol=0
elif yaxis in ['Q22', 'q22', 'q_22', 'Q_22']:
    yaxis="Q22"
    ylabel=r"Triaxiality $\, (\rm{b}) $"
    ycol=1
elif yaxis in ['Q30', 'q30', 'q_30', 'Q_30']:
    yaxis="Q30"
    ylabel=r"Mass Asymmetry $\, (\rm{b}^\frac{3}{2}) $"
    ycol=2
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
    ylabel=r"Mass Asymmetry $\, (\rm{b}^\frac{3}{2}) $"
    ycol=2
print "\n The y-axis will show %s, %s" %(yaxis, ylabel)


dots = raw_input("\n Would you like to draw a dot at every single point from the original data set? This lets you see visually which grid points converged and which ones didn't. \n")

pathway = raw_input("\n Would you like to superimpose a fission pathway onto the PES? \n")
if pathway in ['y', 'Y', 'yes', 'Yes', 'YES']:
    pathfile = raw_input("\n Please list the name of the input file which contains the fission pathway data: \n")


description = raw_input("\n Would you like to include some description text in the top left corner? (eg $^{176}$Pt \\n UNEDF1) \n")
if description in ['y', 'Y', 'yes', 'Yes', 'YES']:
    desctext = raw_input("Please enter your text below: (eg '$^{176}$Pt \\n UNEDF1') \n")

outname = raw_input("\n Please provide a name for the output .eps file [default name 'output']: \n")
if outname=='':
    outname="output"
outfile = "%s.eps" % outname
print "\n The plot will be output to %s. \n" % outfile




#################################
##### Input the data
#################################


data = np.genfromtxt (infilefission, skip_header=1)
x0 = data[:,xcol]
y0 = data[:,ycol]
z0 = data[:,10]

if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    data = np.genfromtxt (infilefusion, skip_header=1)
    x1 = data[:,xcol]
    y1 = data[:,ycol]
    z1 = data[:,10]

if pathway in ['y', 'Y', 'yes', 'Yes', 'YES']:
    data = np.genfromtxt (pathfile)
    x2 = data[:,xcol]
    y2 = data[:,ycol]
    z2 = data[:,3]



#################################
##### Adjust your energy scale to set E=0 at or around Q20=Q30=0
#################################


# Set your origin E=0 to the point in your fission configuration with the minimum energy (hopefully it should be right around Q20=Q30=0)
min_z0 = z0.min()
z0 = z0-min_z0
if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    z1 = z1-min_z0

# Cut out those points which are just skewing the entire graph
index = np.arange(len(z0))
for i in index:
    zval = z0[i]
    if zval > (z0.min ()+cutofffission):
        z0[i]=z0.min ()+cutofffission 

if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
    index = np.arange(len(z1))
    for i in index:
        zval = z1[i]
        if zval > (z0.min ()+cutofffission):
            z1[i]=z0.min ()+cutofffission 


#################################
##### Interpolate your data to fill in holes and give you a nice, smooth contour
#################################


# basis grid for the interpolation
#xi = x0
#yi = y0
xi = np.linspace (min (x0) , max (x0), num=200)
yi = np.linspace (min (y0) , max (y0), num=200)
#xi = np.linspace (0.0 , 345.0)
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
Zplot[Zplot <= -1] = np.nan

maxZplot = np.nanmax (Zplot);
minZplot = np.nanmin (Zplot);


#################################
##### Plot the data
#################################


# APS required dpi, figsize can change
#fig = plt.figure (figsize = (8.0 , 3.0) , dpi = 1200)
fig = plt.figure (figsize = (14 , 6.5) , dpi = 1200)

# add a plot on the figure
ax = fig.add_subplot (111)

# set labels
ax.set_xlabel (xlabel , fontsize=20)
ax.set_ylabel (ylabel , fontsize=20)

# set ticks (min, max, step) gives: [min , min+step , ... , max-step]
tab_range = np.arange (0.0, X0.max(), 100.0)
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
plt.clabel(CS1, inline=1, fontsize=10, colors='k')

# This draws a dot at every single point from the original data set, before they are used to make the interpolated contour. It lets you see visually which grid points converged and which ones didn't.
if dots in ['y', 'Y', 'yes', 'Yes', 'YES']:
    plot (x0, y0, 'k.')
    if lvlcross in ['y', 'Y', 'yes', 'Yes', 'YES']:
        plot (x1, y1, 'g.')

# This plots the fission pathway
if pathway in ['y', 'Y', 'yes', 'Yes', 'YES']:
    plot (x2 , y2, color='blue')



#################################
##### Add some text to the plot
#################################


if description in ['y', 'Y', 'yes', 'Yes', 'YES']:
    text(0.1, 0.9, desctext,
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
#v = np.linspace (round (minZplot , decimal_number) , round (maxZplot + (maxZplot-minZplot)/step , decimal_number) , step , endpoint=True).tolist ()
v = [round (elem , decimal_number) for elem in v] # warning, these are positions of ticks, the "round" function can lead to irregular spacings


# plot the colorbar
cb = plt.colorbar (CS0 , cax=cbar_ax , ticks=v , norm=matplotlib.colors.Normalize (vmin=minZplot , vmax=maxZplot))
cb.set_label(r"Energy $\, (\rm{MeV}) $" , fontsize=20, rotation=270, labelpad=20)

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
matplotlib.rc ('text', usetex=True)


# to add some text on the graph
# not tested
#ax.text (9 , 0 , 0 , "toto" , color='red')
#ax.annotate(r"$ \boldsymbol{ {1/2}^{+} } $" , xy=(6.3 , 6.5) , color='white' , ha='center' , fontsize=23)


# save in ps format, cannot be donne directly in pdf and eps has no bounding box
# follow the instruction below to get a pdf with bounding box
fig.savefig (outfile) # NOTE: This won't work until you've defined "fig."
# in the terminal:
# ps2eps -f test.ps ; epstopdf test.eps


