import numpy as np
import math
import matplotlib.pyplot as plt
import random
from PIL import Image

def BetterSpecAnal(x,plot=False):
	N=64
	x_shape = np.shape(x)
	total_center_window = 5*N
	center_image = x[math.ceil((x_shape[0]-total_center_window)/2):math.ceil((x_shape[0]-total_center_window)/2)+total_center_window,
					math.ceil((x_shape[1]-total_center_window)/2):math.ceil((x_shape[1]-total_center_window)/2)+total_center_window]
	W = np.outer(np.hamming(N), np.hamming(N))

	Sum = np.zeros((N,N))
	for i in range(5):
		for j in range(5):
			sub_fig = center_image[i*N:i*N+N,j*N:j*N+N]
			x_windowed = np.multiply(sub_fig,W)
			Z = (1/N**2)*np.abs(np.fft.fft2(x_windowed))**2
			Sum += Z
	Sum = Sum/25
	Sum = np.fft.fftshift(Sum)
	Sum_abs = np.log(Sum)

	if plot:
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		a = b = np.linspace(-np.pi, np.pi, num = N)
		X, Y = np.meshgrid(a, b)

		surf = ax.plot_surface(X, Y, Sum_abs, cmap=plt.cm.coolwarm)

		ax.set_xlabel('$\mu$ axis')
		ax.set_ylabel('$\\nu$ axis')
		ax.set_zlabel('Average PSD (y)')

		fig.colorbar(surf, shrink=0.5, aspect=5, location="left")
		plt.title('Average PSD after windowing by Hamming window')
		plt.savefig('Power_Spectral_Average_Sectin_2.tif')
		plt.savefig('Power_Spectral_Average_Sectin_2.png')
		plt.show()
	return Sum_abs

def theoretical_PSD(N=128):
	a = b = np.linspace(-np.pi/16, np.pi/16, num = N)
	U,V = np.meshgrid(a, b)
	num = (3*np.sin(U)*np.sin(V)/(U*V))**2
	den = (1-0.99*np.cos(U)-0.99*np.cos(V)+0.9801*np.cos(U+V))**2 + (0.99*np.sin(U)+0.99*np.sin(V)-0.9801*np.sin(U+V))**2
	PSD = num/den
	fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
	ax.plot_surface(U,V,PSD, cmap=plt.cm.coolwarm)
	ax.set_xlabel('$\mu$ axis')
	ax.set_ylabel('$\\nu$ axis')
	ax.set_zlabel('PSD (y)')
	plt.savefig('Power_Spectral_Theoretical.tif')
	plt.savefig('Power_Spectral_Theoretical.png')
	plt.show()

def Main():
	x = np.random.uniform(-0.5,0.5,[512,512])
	x_scaled = np.array(255*(x+0.5))
	print(x_scaled.shape)
	plt.figure()
	plt.imshow(x_scaled)
	plt.colorbar()
	plt.savefig('Random_Image.png')
	plt.show()


	img_out = Image.fromarray(x_scaled)
	img_out.save('Random_Image.tif')


	#Apply the IIR filter
	y = np.ones((x.shape),dtype=np.double)
	print(y.shape)
	for i in range(1,x.shape[0]):
		for j in range(1,x.shape[1]):
			y[i,j] = 0.01*x[i,j] + 0.99*(y[i-1,j]+y[i,j-1]) - 0.9801*y[i-1,j-1]
	print(type(y),'--',np.max(y),'--',np.min(y))

	PSD_y = BetterSpecAnal(y,plot=True)

	y = y +127
	plt.figure()
	plt.imshow(y)
	plt.title('Filtered Image')
	plt.savefig('Filtered Image Section 2.png')

	y = Image.fromarray(y)
	y.save('Filtered Image Section 2.tif')
	plt.colorbar()
	plt.show()
	theoretical_PSD()
Main()
