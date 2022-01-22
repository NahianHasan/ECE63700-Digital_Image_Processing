import os
import matplotlib.pyplot as plt
import numpy as np
import math

#For FIR Filter in section 3

U = np.linspace(-np.pi,np.pi,1000)
V = np.linspace(-np.pi,np.pi,1000)
u,v = np.meshgrid(U,V)
H = 1/81*(1 + np.cos(4*v) + 2*np.cos(3*v) + 2*np.cos(2*v) + 2*np.cos(v)) * (1 + np.cos(4*u) + 2*np.cos(3*u) + 2*np.cos(2*u) + 2*np.cos(u))
H_mag = np.abs(H)
fig = plt.figure()
ax = plt.axes(projection='3d')
surf = ax.plot_surface(u, v, H_mag,cmap='viridis', edgecolor='none')
ax.set_xlabel('u')
ax.set_ylabel('v')
ax.set_zlabel('|H|')
fig.colorbar(surf,location = 'left')
plt.savefig('./output/python_FIR_3.tif')
plt.savefig('./output/python_FIR_3.png')
#plt.show()


#For FIR Filter in section 4
U = np.linspace(-np.pi,np.pi,1000)
V = np.linspace(-np.pi,np.pi,1000)
u,v = np.meshgrid(U,V)
H = 1/25*(1 + 2*np.cos(2*v) + 2*np.cos(v)) * (1 + 2*np.cos(2*u) + 2*np.cos(u))
H_mag = np.abs(H)
fig = plt.figure()
ax = plt.axes(projection='3d')
surf = ax.plot_surface(u, v, H_mag,cmap='viridis', edgecolor='none')
ax.set_xlabel('u')
ax.set_ylabel('v')
ax.set_zlabel('|H|')
fig.colorbar(surf,location = 'left')
plt.savefig('./output/python_FIR_4.tif')
plt.savefig('./output/python_FIR_4.png')
#plt.show()


#For FIR Filter, sharpening filter, in section 4
L = 1.5#lambda
G = 1+L*(1-H)
G_mag = np.abs(G)
fig = plt.figure()
ax = plt.axes(projection='3d')
surf = ax.plot_surface(u, v, G_mag,cmap='viridis', edgecolor='none')
ax.set_xlabel('u')
ax.set_ylabel('v')
ax.set_zlabel('|G|')
fig.colorbar(surf,location = 'left')
plt.savefig('./output/python_FIR_4_sharpening.tif')
plt.savefig('./output/python_FIR_4_sharpening.png')
#plt.show()


#For IIR Filter, in section 5
U = np.linspace(-np.pi,np.pi,1000)
V = np.linspace(-np.pi,np.pi,1000)
u,v = np.meshgrid(U,V)
H = 0.01/(1-0.9*(np.exp(-1j*u)+np.exp(-1j*v)) + 0.81*np.exp(-1j*(u+v)))
H_mag = np.abs(H)
fig = plt.figure()
ax = plt.axes(projection='3d')
surf = ax.plot_surface(u, v, H_mag,cmap='viridis', edgecolor='none')
ax.set_xlabel('u')
ax.set_ylabel('v')
ax.set_zlabel('|H|')
fig.colorbar(surf,location = 'left')
plt.savefig('./output/python_IIR.tif')
plt.savefig('./output/python_IIR.png')
#plt.show()
