import matplotlib.pyplot as plt
import numpy as np

def calculate_RMSE(X,Y):
	X = X.astype(float)
	Y = Y.astype(float)
	RMSE = np.sqrt(np.sum(np.power(X-Y,2))/np.prod(X.shape))
	return RMSE

def fidelity(X,Y,gamma,verbose=False):
	X_g_corrected = 255*np.power(X/255,gamma)
	X_b_g_corrected = 255*np.power(Y/255,gamma)
	plt.figure()
	plt.subplot(121)
	plt.imshow(X_g_corrected,cmap='gray')
	plt.title('Gamma Corrected Original')
	plt.subplot(122)
	plt.imshow(X_b_g_corrected,cmap='gray',interpolation='none')
	plt.title('Gamma Corrected Binary')
	plt.savefig('Gamma_Corrected_Image.png')

	X_filtered = np.zeros(X_g_corrected.shape)
	X_b_filtered = np.zeros(X_b_g_corrected.shape)

	#Low Pass FIlter
	X_g_corrected = np.pad(X_g_corrected,((3,3),(3,3)),mode='constant')
	X_b_g_corrected = np.pad(X_b_g_corrected,((3,3),(3,3)),mode='constant')
	normalizing_constant = 0.08143899724403883
	for i in range(3,X_g_corrected.shape[0]-3):
		for j in range(3,X_g_corrected.shape[1]-3):
			sum1 = 0
			sum2 = 0
			for k in range(i-3,i+4):
				for l in range(j-3,j+4):
					sum1 = sum1 + np.exp(-((k-i)*(k-i)+(l-j)*(l-j))/4) * X_g_corrected[k,l]
					sum2 = sum2 + np.exp(-((k-i)*(k-i)+(l-j)*(l-j))/4) * X_b_g_corrected[k,l]
			sum1 *= normalizing_constant
			sum2 *= normalizing_constant
			X_filtered[i-3,j-3] = sum1
			X_b_filtered[i-3,j-3] = sum2
	plt.figure()
	plt.subplot(121)
	plt.imshow(X_filtered,cmap='gray')
	plt.title('Filtered Original')
	plt.subplot(122)
	plt.imshow(X_b_filtered,cmap='gray',interpolation='none')
	plt.title('Filtered Binary')
	plt.savefig('Filtered_Image.png')
	if verbose:
		plt.show()
	X_filtered = 255*np.power(X_filtered/255,1/3)
	X_b_filtered = 255*np.power(X_b_filtered/255,1/3)

	fid = calculate_RMSE(X_filtered,X_b_filtered)
	return fid
