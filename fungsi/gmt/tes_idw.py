import numpy as np
import matplotlib.pyplot as plt
import csv
from pandas import *



def distance_matrix(x0, y0, x1, y1):
    
    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T

    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])
    
    # calculate hypotenuse
    return np.hypot(d0, d1)

def simple_idw(x, y, z, xi, yi, power=1):
    
    
    dist = distance_matrix(x,y, xi,yi)

    # In IDW, weights are 1 / distance
    weights = 1.0/(dist+1e-12)**power

    # Make weights sum to one
    weights /= weights.sum(axis=0)

    # Multiply the weights for each interpolated point by all observed Z-values
    return np.dot(weights.T, z)

def plot(x,y,z,grid):
    """ Plot the input points and the result """
    plt.figure(figsize=(10,10))
    plt.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()), cmap='jet',
               interpolation='gaussian')
    plt.scatter(x,y,c=z, cmap='rainbow', edgecolors='black')
    # plt.colorbar()

data = read_csv("tesblok.xyz", sep='\t', names=['x', 'y', 'z'])
x = data['x'].tolist()
y = data['y'].tolist()
z = data['z'].tolist()
# print(fz)

# x = [100,200,300,400,100,200,300,400,100,200,300,400,100,200,300,400]
# y = [100,100,100,100,200,200,200,200,300,300,300,300,400,400,400,400]
# z = [1,2,5,0,5,0,12,0,4,3,2,2,1,5,7,9]
x = np.array(x)
y = np.array(y)
z = np.array(z)
# size of the grid to interpolate
nx, ny = 112,112

# generate two arrays of evenly space data between ends of previous arrays
xi = np.linspace(x.min(), x.max(), nx)
yi = np.linspace(y.min(), y.max(), ny)

# generate grid 
xi, yi = np.meshgrid(xi, yi)

# colapse grid into 1D
xi, yi = xi.flatten(), yi.flatten()


 # Calculate IDW
grid1 = simple_idw(x,y,z,xi,yi, power=2)
grid2 = grid1.reshape((ny, nx))
plot(x,y,z,grid2)
# print(len(grid1))
# print(len(x))
# print(len(y))

# print(xi)
# print(yi)
# print(grid2)
lst=list(zip(xi,yi,grid1))
# print(len(lst))
# print(lst)
# plt.title('Simple IDW power=1')
# plt.show()
# plt.axis('off')
plt.savefig('tesidw.png')
plt.savefig('tesidw.svg')

with open('tes_idw.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file,delimiter ='\t')
    writer.writerows(lst) # Use writerows for nested list

# gmt blockmean sambaran.dat -R127/128/0.3/1.3 -I1k -Sn | gmt xyz2grd -R127/128/0.3/1.3 -I1k -Gtesblok.grd
# gmt grd2xyz tesblok.grd -d0> tesblok.xyz

# gmt grdimage tesidwcut.grd -JM -R -Q -Ckerapatan.cpt -t30  > tesidw.ps
# gmt psconvert tesidw.ps -TG -A -P -E256
# gmt surface tes_idw.csv -R127/128/0.3/1.3 -I100e -Gtesidwsurf.grd=sf -T0.25 -fg
# gmt grdsample tesidwsurf.grd -I1s -Gtesidwsamp.grd
# gmt grdclip tesidwsamp.grd -R -Sb1/NaN -Gtesidwcut.grd
 # Calculate IDW
# grid1 = simple_idw(x,y,z,xi,yi, power=2)
# grid1 = grid1.reshape((ny, nx))
# plot(x,y,z,grid1)
# plt.title('Simple IDW power=2')
# plt.show()