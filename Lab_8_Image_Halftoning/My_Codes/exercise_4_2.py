### Ordered Dithering ##########
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import utils as U

def Bayer_Index_Matrix(IN):
	I2N=np.block([[4*IN + 1,4*IN + 2],[4*IN + 3,4*IN]])
	return I2N

def Threshold_Matrix(I):
	T = np.zeros(I.shape)
	for i in range(0,I.shape[0]):
		for j in range(0,I.shape[1]):
			T[i,j] = 255 * (I[i,j] + 0.5)/np.prod(I.shape)
	return T

def Tiled_Matrix(T,width,height):
	width_factor = int(np.ceil(width/T.shape[1]))
	height_factor = int(np.ceil(height/T.shape[0]))
	T = np.tile(T,(height_factor,width_factor))
	return T

def Main():
	name = '../house.tif'
	im = Image.open(name)
	X = np.array(im)
	gamma = 2.2

	X_g_corrected = 255*np.power(X/255,gamma)
	#Form Bayer Index Matrices
	I_2 = np.array([[1,2],[3,0]])
	I_4 = Bayer_Index_Matrix(I_2)
	I_8 = Bayer_Index_Matrix(I_4)
	T_2 = Threshold_Matrix(I_2)
	T_4 = Threshold_Matrix(I_4)
	T_8 = Threshold_Matrix(I_8)
	print(I_2)
	print(I_4)
	print(I_8)
	#print(T_2)
	#print(T_4)
	#print(T_8)

	T_2_tiled = Tiled_Matrix(T_2,X.shape[1],X.shape[0])
	T_4_tiled = Tiled_Matrix(T_4,X.shape[1],X.shape[0])
	T_8_tiled = Tiled_Matrix(T_8,X.shape[1],X.shape[0])
	#print(T_2_tiled.shape)
	#print(T_4_tiled.shape)
	#print(T_8_tiled.shape)

	HT_2 = np.where(X_g_corrected > T_2_tiled, 255, 0)
	HT_4 = np.where(X_g_corrected > T_4_tiled, 255, 0)
	HT_8 = np.where(X_g_corrected > T_8_tiled, 255, 0)

	plt.figure()
	plt.subplot(221)
	plt.imshow(X_g_corrected,cmap='gray')
	plt.title('Gamma Corrected Original',fontsize=8)
	plt.subplot(222)
	plt.imshow(HT_2,cmap='gray',interpolation='none')
	plt.title('Halftone, Dither Matrix Order = 2',fontsize=8)
	plt.subplot(223)
	plt.imshow(HT_4,cmap='gray',interpolation='none')
	plt.title('Halftone, Dither Matrix Order = 4',fontsize=8)
	plt.subplot(224)
	plt.imshow(HT_8,cmap='gray',interpolation='none')
	plt.title('Halftone, Dither Matrix Order = 8',fontsize=8)
	plt.savefig('Ordered_Dithering.png')

	#save images as tif files
	img_out = Image.fromarray(HT_2.astype(np.uint8))
	img_out.save('Half_tone_D_2.tif')
	img_out = Image.fromarray(HT_4.astype(np.uint8))
	img_out.save('Half_tone_D_4.tif')
	img_out = Image.fromarray(HT_8.astype(np.uint8))
	img_out.save('Half_tone_D_8.tif')
	img_out = Image.fromarray(X_g_corrected.astype(np.uint8))
	img_out.save('Gamma_Corrected_Original.tif')
	img_out = Image.fromarray(X.astype(np.uint8))
	img_out.save('Original_Image.tif')

	#Compute RMSE and fidelity
	RMSE_2, RMSE_4, RMSE_8 = U.calculate_RMSE(X,HT_2), U.calculate_RMSE(X,HT_4), U.calculate_RMSE(X,HT_8)
	fidelity_2, fidelity_4, fidelity_8 = U.fidelity(X,HT_2,gamma,verbose=False), U.fidelity(X,HT_4,gamma,verbose=False), U.fidelity(X,HT_8,gamma,verbose=False)
	print('RMSE_2 = ',RMSE_2)
	print('RMSE_4 = ',RMSE_4)
	print('RMSE_8 = ',RMSE_8)
	print('Fidelity_2 = ',fidelity_2)
	print('Fidelity_4 = ',fidelity_4)
	print('Fidelity_8 = ',fidelity_8)

Main()
