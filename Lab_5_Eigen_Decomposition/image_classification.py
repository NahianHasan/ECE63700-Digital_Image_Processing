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

N = 10#N=number of eigenvectors to consider
A = U[:,0:N]
Y = np.matmul(np.transpose(A),X)
print('Y = ',Y.shape)

class_mean = list()
class_cov = list()
for i in range(0,26):
	class_images = []
	count = 0
	for j in range(i,Y.shape[1],26):
		class_images.append(Y[:,j])
		count += 1

	class_images = np.array(class_images)
	class_images = class_images.T
	cm = np.reshape(np.sum(class_images,1)/count,[N,1])
	class_mean.append(cm)
	class_cov.append(np.matmul((class_images-cm),np.transpose(class_images-cm))/(count-1))

class_mean = (np.array(class_mean)).squeeze()
class_cov = (np.array(class_cov)).squeeze()
print('Class Mean = ',class_mean.shape)
print('Class Covariance = ',class_cov.shape)


############ Test data Read  ########################
datadir='../test_data'    # directory where the data files reside
dataset=['veranda']
datachar='abcdefghijklmnopqrstuvwxyz'
Rows=64    # all images are 64x64
Cols=64
n=len(dataset)*len(datachar)  # total number of images
p=Rows*Cols   # number of pixels

X_test=np.zeros((p,n))  # images arranged in columns of X
k=0
for dset in dataset:
	for ch in datachar:
		fname='/'.join([datadir,dset,ch])+'.tif'
		im=Image.open(fname)
		img = np.array(im)
		X_test[:,k]=np.reshape(img,(1,p))
		k+=1
print('X_test = ',X_test.shape)
X_test -= X_mean
Y_test = np.matmul(np.transpose(A),X_test)
print('Y_test = Y',Y_test.shape)

def calculate_distance(Y_test,class_mean,class_cov):
	correct_table = list()
	incorrect_table = list()
	for i in range(0,Y_test.shape[1]):
		distance = list()
		for c in range(class_mean.shape[0]):
			T = np.reshape(Y_test[:,i] - np.transpose(class_mean[c,:]), [N,1])
			distance.append(np.matmul(np.transpose(T),np.matmul(np.linalg.inv(class_cov[c,:,:]),T)) + np.log(np.linalg.norm(class_cov[c,:,:])))
		distance = list((np.array(distance)).squeeze())
		predicted_class = datachar[distance.index(np.min(distance))]
		if datachar[i] == predicted_class:
			correct_table.append([datachar[i],predicted_class])
		else:
			incorrect_table.append([datachar[i],predicted_class])
	return correct_table,incorrect_table

[correct_table,incorrect_table] = calculate_distance(Y_test,class_mean,class_cov)
print('\n\nOriginal Covariance - Incorrect Classes')
for i in range(0,len(incorrect_table)):
	print(incorrect_table[i][0],' ------------------------- ',incorrect_table[i][1])
print('\n')
########### Modification 1 ##############
modified_cov = list()
for i in range(0,class_cov.shape[0]):
	modified_cov.append(np.diag(np.diag(class_cov[i,:,:])))
modified_cov = np.array(modified_cov)
[correct_table,incorrect_table] = calculate_distance(Y_test,class_mean,modified_cov)
print('Modification 1 - Incorrect Classes')
for i in range(0,len(incorrect_table)):
	print(incorrect_table[i][0],' ------------------------- ',incorrect_table[i][1])
print('\n')


########### Modification 2 ##############
modified_cov = list()
avg_cov = np.sum(class_cov,0)/class_cov.shape[0]
for i in range(0,class_cov.shape[0]):
	modified_cov.append(avg_cov)
modified_cov = np.array(modified_cov)
print('Modification 2 - Incorrect Classes')
[correct_table,incorrect_table] = calculate_distance(Y_test,class_mean,modified_cov)
for i in range(0,len(incorrect_table)):
	print(incorrect_table[i][0],' ------------------------- ',incorrect_table[i][1])
print('\n')
########### Modification 3 ##############
modified_cov = list()
avg_cov = np.sum(class_cov,0)/class_cov.shape[0]
for i in range(0,class_cov.shape[0]):
	modified_cov.append(np.diag(np.diag(avg_cov)))
modified_cov = np.array(modified_cov)
print('Modification 3 - Incorrect Classes')
[correct_table,incorrect_table] = calculate_distance(Y_test,class_mean,modified_cov)
for i in range(0,len(incorrect_table)):
	print(incorrect_table[i][0],' ------------------------- ',incorrect_table[i][1])
print('\n')
########### Modification 4 ##############
modified_cov = list()
for i in range(0,class_cov.shape[0]):
	modified_cov.append(np.identity(class_cov.shape[1]))
modified_cov = np.array(modified_cov)
print('Modification 4 - Incorrect Classes')
[correct_table,incorrect_table] = calculate_distance(Y_test,class_mean,modified_cov)
for i in range(0,len(incorrect_table)):
	print(incorrect_table[i][0],' ------------------------- ',incorrect_table[i][1])
print('\n')
