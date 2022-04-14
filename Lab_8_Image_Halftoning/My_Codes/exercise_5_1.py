### Ordered Dithering ##########
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import utils as U

def Diffusion_Error(I,T):
	Im_out = np.zeros(I.shape)
	print(I.shape)
	I = np.pad(I,((1,1),(1,1)))
	print(I.shape)
	for i in range(1,I.shape[0]-1):
		for j in range(1,I.shape[1]-1):
			Im_out[i-1,j-1] = 255 if I[i,j] > T else 0
			error = I[i,j] - Im_out[i-1,j-1]
			I[i,j+1] = I[i,j+1]+7/16*error
			I[i+1,j-1] = I[i+1,j-1]+3/16*error
			I[i+1,j] = I[i+1,j]+5/16*error
			I[i+1,j+1] = I[i+1,j+1]+1/16*error
	return Im_out

def Main():
	name = '../house.tif'
	im = Image.open(name)
	X = np.array(im)
	gamma = 2.2
	Threshold = 127

	X_g_corrected = 255*np.power(X/255,gamma)
	Im_out = Diffusion_Error(X_g_corrected,Threshold)
	RMSE = U.calculate_RMSE(X,Im_out)
	fidelity = U.fidelity(X,Im_out,gamma,verbose=False)
	print('RMSE = ',RMSE)
	print('Fidelity = ',fidelity)

	Im_out = Image.fromarray(Im_out.astype(np.uint8))
	Im_out.save('Error_Diffusion.tif')
Main()
