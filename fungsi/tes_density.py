import matplotlib.pyplot as plt
import numpy as np
from pandas import *
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import cm
import csv
# import xlrd

data = read_csv("gmt/sambaran.dat", sep=' ',header=None)
x=data[0].to_list()
y=data[1].to_list()
# x=[127.1,127.12,127.9,127.95,127.98,127.1,127.12,127.14,127.18,127.2,127.86,127.88,127.9,127.92,127.95,127.98]
# y=[0.5  ,0.5   ,0.5  ,0.5   ,0.5   ,1.3  ,1.3   ,1.3   ,1.3   ,1.3  ,1.3   ,1.3   ,1.3   ,1.3   ,1.3   ,1.3]
nx,ny = 27,27
lon_bins = np.linspace(127,128,nx+1)
lat_bins = np.linspace(0.4,1.4,ny+1)

density, _, _ = np.histogram2d(x,y,[lon_bins,lat_bins])
density = np.divide(density,16)


viridis = cm.get_cmap('viridis', 4)
newcolors = viridis(np.linspace(0, 1, 4))
red = np.array([256/256, 0/256, 0/256, 1])
green = np.array([0/256, 256/256, 0/256, 1])
blue = np.array([0/256, 0/256, 256/256, 1])
new = np.linspace(1.0,0.0,4)
newcolors[:1, :] = red
newcolors[1:2, :] = green
newcolors[2:3, :] = blue
newcolors[:4, :] =  new
newcmp = ListedColormap(newcolors)
cmap = ListedColormap([np.linspace(1.0,0.0,4), 'g', 'y','r'])
norm = BoundaryNorm([0,0.9,2,3,120], cmap.N)

density = np.flip(density,1)
print(density)
print(lon_bins,lat_bins)
plt.figure(figsize=(10,10))
# plt.imshow(density.T, extent=(127, 128, 1.4, 0.4), cmap='rainbow',interpolation='gaussian')
plt.imshow(density.T, extent=(127, 128, 0.4, 1.4), cmap=cmap, norm=norm,
               interpolation='spline36')
plt.scatter(x,y, edgecolors='black',s=10)
# plt.axis('off')
plt.savefig('tesdensity.png',)
# a = map.imshow(density.T, interpolation='spline36', alpha=1, cmap='YlOrBr',vmin=0,vmax=15)