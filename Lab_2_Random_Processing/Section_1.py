import numpy as np                 # Numpy is a library support computation of large, multi-dimensional arrays and matrices.
from PIL import Image              # Python Imaging Library (abbreviated as PIL) is a free and open-source additional library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats.
import matplotlib.pyplot as plt    # Matplotlib is a plotting library for the Python programming language.
import math

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
		ax.set_zlabel('Average PSD')

		fig.colorbar(surf, shrink=0.5, aspect=5, location="left")
		plt.title('Average PSD after windowing by Hamming window')
		plt.savefig('Power_Spectral_Average.tif')
		plt.savefig('Power_Spectral_Average.png')
		plt.show()
	return Sum_abs

def Main():
	# Read in a gray scale TIFF image.
	im = Image.open('img04g.tif')
	print('Read img04.tif.')
	print('Image size: ', im.size)
	x = np.array(im)
	x = np.double(x)/255.0
	S = BetterSpecAnal(x,plot=True)

Main()
