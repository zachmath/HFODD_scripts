# To find the total particle density in the neck

from matplotlib.pyplot import figure , axes , plot , xlabel , ylabel , title , grid , savefig , show
import numpy as np
from pylab import *
from scipy import integrate



# get data
data = np.genfromtxt ('densi_000088.out') # Columns are: x, y, z, rho_p, rho_n, rho_tot
x0 = data[:,0]
y0 = data[:,1]
z0 = data[:,2]
rho0 = data[:,5]

# You'll want some kind of range, so you can focus on counting only particles in a specific region.
# Default is to use the full range, but you can put your own values in, too.

x_min = 0.0 #np.min(abs(x0))
x_max = 0.3 #np.max(abs(x0))
x = x0[(abs(x0) >= x_min) & (abs(x0) <= x_max)]
y = y0[(abs(x0) >= x_min) & (abs(x0) <= x_max)]
z = z0[(abs(x0) >= x_min) & (abs(x0) <= x_max)]
rho = rho0[(abs(x0) >= x_min) & (abs(x0) <= x_max)]

y_min = 0.0 #np.min(abs(y0))
y_max = 0.3 #np.max(abs(y0))
x = x[(abs(y) >= y_min) & (abs(y) <= y_max)]
y = y[(abs(y) >= y_min) & (abs(y) <= y_max)]
z = z[(abs(y) >= y_min) & (abs(y) <= y_max)]
rho = rho[(abs(y) >= y_min) & (abs(y) <= y_max)]

z_min = 0.0 #np.min(abs(z0))
z_max = 0.4 #np.max(abs(z0))
x = x[(abs(z) >= z_min) & (abs(z) <= z_max)]
y = y[(abs(z) >= z_min) & (abs(z) <= z_max)]
z = z[(abs(z) >= z_min) & (abs(z) <= z_max)]
rho = rho[(abs(z) >= z_min) & (abs(z) <= z_max)]

# Let's make a list of all the possible x, y, and z values (but one that isn't repeated several thousand times). It'll be nice to have later.

x_list = [0]
y_list = [0]
z_list = [0]

for i in range(np.size(x)):
	if x[i] not in x_list:
		x_list = x_list + [x[i]]
	if y[i] not in y_list:
		y_list = y_list + [y[i]]
	if z[i] not in z_list:
		z_list = z_list + [z[i]]

x_list = sorted(x_list)
y_list = sorted(y_list)
z_list = sorted(z_list)

# Now you find perform a weighted sum, basically, where the density gets multiplied by the size of its corresponding box (not all boxes are the same size since the grid points are unevenly-spaced, hence "weighted")

num_particles = 0


for i in range(np.size(x)):

	index_x = x_list.index(abs(x[i]))
	x_prev = x_list[index_x - 1]
	delta_x = abs(x[i] - x_prev)

	index_y = y_list.index(abs(y[i]))
	y_prev = y_list[index_y - 1]
	delta_y = abs(y[i] - y_prev)

	index_z = z_list.index(abs(z[i]))
	z_prev = z_list[index_z - 1]
	delta_z = abs(z[i] - z_prev)

	num_particles += rho[i] * delta_x * delta_y * delta_z

print num_particles
