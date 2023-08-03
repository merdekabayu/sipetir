import numpy as np
import matplotlib.pyplot as plt
import csv
from pandas import *
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import cm



def distance_matrix(x0, y0, x1, y1):
    
    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T
    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])
    # calculate hypotenuse
    return np.hypot(d0, d1)

def simple_idw(x, y, z, xi, yi, power):
    dist = distance_matrix(x,y, xi,yi)
    # In IDW, weights are 1 / distance
    weights = 1.0/(dist+1e-12)**power
    # Make weights sum to one
    weights /= weights.sum(axis=0)
    # Multiply the weights for each interpolated point by all observed Z-values
    return np.dot(weights.T, z)

def plot(x,y,z,grid):
    """ Plot the input points and the result """
    
    cmap = ListedColormap([np.linspace(1.0,0.0,4), 'g', 'y','r'])
    norm = BoundaryNorm([0,0.2,3,4,10], cmap.N)
    plt.figure(figsize=(10,10))
    plt.imshow(grid, extent=(x.min(), x.max(), y.min(), y.max()), cmap=cmap, norm=norm,
               interpolation='gaussian')



data = read_csv("fungsi/gmt/sambaran.xyz", sep='\t', names=['x', 'y', 'z'])
x,y,z = data['x'].tolist(),data['y'].tolist(),data['z'].tolist()
x = np.array(x)
y = np.array(y)[::-1]
z = np.array(z)
print(z.max(),z.min())

# size of the grid to interpolate
nx, ny = 110,110
# generate two arrays of evenly space data between ends of previous arrays
xi = np.linspace(x.min(), x.max(), nx)
yi = np.linspace(y.min(), y.max(), ny)
# generate grid 
xi, yi = np.meshgrid(xi, yi)
# colapse grid into 1D
xi, yi = xi.flatten(), yi.flatten()
 # Calculate IDW
grid1 = simple_idw(x,y,z,xi,yi, power=5)
grid2 = grid1.reshape((ny, nx))

plot(x,y,z,grid2)
yi=yi[::-1]
lst=list(zip(xi,yi,grid1))

with open('fungsi/idw.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file,delimiter ='\t')
    writer.writerows(lst) # Use writerows for nested list


# plt.title('Simple IDW power=1')
# plt.show()
# data1 = read_csv("gmt/sambaran.dat", sep=' ',header=None)
# xs=data1[0].to_numpy()
# ys=data1[1].to_numpy()

# plt.scatter(xs,ys, edgecolors='black',s=10)
# # plt.axis('off')
# plt.savefig('tesidw.png')
# plt.savefig('tesidw.png', transparent=True, bbox_inches='tight',pad_inches=0)

# gmt blockmean sambaran.dat -R127/128/0.3/1.3 -I1k -Sn | gmt xyz2grd -R127/128/0.3/1.3 -I1k -Gtesblok.grd
# gmt grd2xyz tesblok.grd -d0> tesblok.xyz

# gmt grdimage tesidwcut.grd -JM -R -Q -Ckerapatan.cpt -t30  > tesidw.ps
# gmt psconvert tesidw.ps -TG -A -P -E256
# gmt surface tes_idw.csv -R127/128/0.3/1.3 -I100e -Gtesidwsurf.grd=sf -T0.25 -fg
# gmt grdsample tesidwsurf.grd -I1s -Gtesidwsamp.grd
# gmt grdclip tesidwsamp.grd -R -Sb1/NaN -Gtesidwcut.grd
