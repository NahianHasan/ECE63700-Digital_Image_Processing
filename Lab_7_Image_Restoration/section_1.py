import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

noisy_image = ['img14sp']#'img14gn', 'img14sp', 'img14bl'
for im in noisy_image:
	Y = np.array(Image.open('../images-restoration/img14g.tif')).astype(float)
	X = np.array(Image.open('../images-restoration/'+im+'.tif')).astype(float)
	X_shape = X.shape
	print('Y = ',Y.shape)
	print('X = ',X.shape)
	window_shape = [7,7]
	pos_ind = int(np.floor(7/2))

	#X = np.pad(X,((pos_ind,pos_ind),(pos_ind,pos_ind)),'constant', constant_values=(0,0))
	print('X_padded = ',X.shape)
	Zs = list()
	Ys = list()
	pix_count = 0
	for i in range(pos_ind,X.shape[0]-pos_ind):
		for j in range(pos_ind,X.shape[1]-pos_ind):
			pix_count += 1
			if pix_count==400:
				Zs.append(np.reshape(X[i-pos_ind:i+pos_ind+1,j-pos_ind:j+pos_ind+1],[1,np.prod(window_shape)]))
				Ys.append(Y[i-pos_ind,j-pos_ind])
				pix_count = 0

	Zs = np.array(Zs).astype(float)
	Ys = np.array(Ys).astype(float)
	Zs = np.reshape(Zs,[Zs.shape[0],Zs.shape[-1]])
	Ys = np.reshape(Ys,[len(Ys),1])
	print('Zs = ',Zs.shape)
	print('Ys = ',Ys.shape)
	M = Ys.shape[0]#number of selected pixels
	print('Number of sampled pixels = ',M)
	R = np.matmul(Zs.T,Zs)/M
	r = np.matmul(Zs.T,Ys)/M
	print('R = ',R.shape)
	print('r = ',r.shape)

	theta = np.matmul(np.linalg.inv(R),r)
	print('theta = ',theta.shape)
	print(np.sum(theta))
	print(np.reshape(theta,window_shape))
	filtered_image = np.zeros(X_shape)
	for i in range(pos_ind,X.shape[0]-pos_ind):
		for j in range(pos_ind,X.shape[1]-pos_ind):
			t = np.reshape(X[i-pos_ind:i+pos_ind+1,j-pos_ind:j+pos_ind+1],[1,np.prod(window_shape)])
			filtered_image[i-pos_ind,j-pos_ind] = np.matmul(t,theta)
	print('filtered_image = ',filtered_image.shape)
	filtered_image = Image.fromarray(filtered_image.astype(np.uint8))
	filtered_image.save(im+'_filtered.tif')
