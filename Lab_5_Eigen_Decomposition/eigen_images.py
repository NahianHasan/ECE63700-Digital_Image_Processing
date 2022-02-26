import read_data as RD
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

X = RD.read_data()
print('X = ',X.shape)
X_mean = np.reshape(np.sum(X,1)/X.shape[1],[ X.shape[0],1])
X = X-X_mean
print('X_centerred = ',X.shape)
[U,S,V] = np.linalg.svd(X, full_matrices=False)
print('U = ',U.shape)
print('S = ',S.shape)
print('V = ',V.shape)

N = 12#number of eigen images
Eig_im = U[:,0:N]
plt.figure(figsize=(10,10))
for i in range(0,N):
	plt.subplot(int(np.sqrt(N)),int(np.ceil(N/int(np.sqrt(N)))),i+1)
	im = np.reshape(Eig_im[:,i],[64,64])
	plt.imshow(im,cmap=plt.cm.gray, interpolation='none')
	plt.title('Eigen Image = '+str(i+1))

plt.savefig('Eigen_Images.png')
plt.savefig('Eigen_Images.tif')

Y = np.matmul(np.transpose(U),X)
print('Y = ',Y.shape)
plt.figure(figsize=(10,10))
Np = 10#Number of projection coefficients to plot
Ni = 4#Number of images
images = ['a','b','c','d']
for i in range(0,Ni):
	plt.plot(np.arange(1,Np+1),Y[0:Np,i],label='Image = '+images[i])
plt.xlabel('Eigenvectors',fontsize=20)
plt.xticks(weight = 'bold',fontsize=15)
plt.ylabel('Magnitude of the projection coefficient',fontsize=20)
plt.yticks(weight = 'bold',fontsize=15)
plt.legend(fontsize=20)
plt.savefig('Projection_Coefficients.png')
plt.savefig('Projection_Coefficients.tif')

#Image synthesis
ind = 0#index of the image to synthesize
m = [1, 5, 10, 15, 20, 30]
plt.figure(figsize=(10,15))
for i in range(0,len(m)):
	X_hat = np.reshape(np.matmul(U[:,0:m[i]],Y[0:m[i],ind]),[X.shape[0],1])
	print(X_hat.shape)
	print(X_mean.shape)
	X_hat += X_mean
	plt.subplot(3,2,i+1)
	im = np.reshape(X_hat,[64,64])
	plt.imshow(im,cmap=plt.cm.gray, interpolation='none')
	plt.title('m = '+str(m[i]),fontsize=20)
	plt.xticks(weight = 'bold',fontsize=15)
	plt.yticks(weight = 'bold',fontsize=15)
	#img_out = Image.fromarray(im.astype(np.uint8))
	#img_out.save('Im_reconstruction_'+str(m[i])+'.tif')
plt.savefig('Im_reconstruction.png')
plt.savefig('Im_reconstruction.tif')
