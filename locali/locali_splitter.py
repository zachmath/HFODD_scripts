import os, math
import numpy as np

infile = 'local_000007.out'

neu_up = open('local_neu_up_249-22.out','w')
neu_dw = open('local_neu_dw_249-22.out','w')
pro_up = open('local_pro_up_249-22.out','w')
pro_dw = open('local_pro_dw_249-22.out','w')

col_width = 18

x0, y0, z0, loc_up, loc_down = [], [], [], [], []

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

# get neutron data
with open(infile) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'NEUTRON LOCALIZATION':  # Or whatever test is needed
            break
    # Reads text until the end of the neutron block:
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


for row in zip(x0,y0,loc_up,loc_down):
            x,y,lup,ldw = row[0],row[1],row[2],row[3]
            row_up = [x] + [y] + [lup]
            row_dw = [x] + [y] + [ldw]
            neu_up.write( "".join(str(word).center(col_width) for word in row_up) )
            neu_up.write('\n')
            neu_dw.write( "".join(str(word).center(col_width) for word in row_dw) )
            neu_dw.write('\n')

neu_up.close()
neu_dw.close()

##########  END NEUTRONS ##############

########## BEGIN PROTONS ##############

x0, y0, z0, loc_up, loc_down = [], [], [], [], []

# get proton data
with open(infile) as input_data:
    # Skips text before the beginning of the interesting block:
    for line in input_data:
        if line.strip() == 'PROTON LOCALIZATION':  # Or whatever test is needed
            break
    # Reads text until the end of the neutron block:
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


for row in zip(x0,y0,loc_up,loc_down):
            x,y,lup,ldw = row[0],row[1],row[2],row[3]
            row_up = [x] + [y] + [lup]
            row_dw = [x] + [y] + [ldw]
            pro_up.write( "".join(str(word).center(col_width) for word in row_up) )
            pro_up.write('\n')
            pro_dw.write( "".join(str(word).center(col_width) for word in row_dw) )
            pro_dw.write('\n')

pro_up.close()
pro_dw.close()




