from PIL import Image
import matplotlib.pyplot as plt
import utils as U
import numpy as np

def Main():
	name = '../house.tif'
	im = Image.open(name)
	X = np.array(im)
	threshold = 127

	plt.figure()
	plt.subplot(121)
	plt.imshow(X,cmap='gray')
	plt.title('Original')
	X_b = np.where(X > threshold, 255,0)
	img_out = Image.fromarray(X_b.astype(np.uint8))
	img_out.save('binary_thresholding.tif')
	plt.subplot(122)
	plt.imshow(X_b,cmap='gray',interpolation='none')
	plt.title('Binary')
	plt.savefig('Original_vs_Binary_Image.png')

	RMSE = U.calculate_RMSE(X,X_b)
	print('RMSE = ',RMSE)

	gamma = 2.2
	fid = U.fidelity(X,X_b,gamma,verbose=False)
	print('Fidelity = ',fid)

Main()
