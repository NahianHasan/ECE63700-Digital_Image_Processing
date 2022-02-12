import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from PIL import Image
from skimage import exposure
from PIL import Image
import cv2

##########   Section 1 from skimage import exposure ###########################################
def plot_histogram(x,cmap,name,save_path,L):
	plt.figure()
	plt.subplot(121)
	plt.imshow(x,cmap=cmap)
	plt.title(name)
	plt.subplot(122)
	plt.hist(x.flatten(),bins=np.linspace(0,255,L))
	plt.title(save_path)
	plt.savefig(save_path+'.tif')
	plt.savefig(save_path+'.png')
def section_1():
	L=256
	gray = cm.get_cmap('gray', L)
	im = Image.open ('race.tif')
	x = np.array(im)
	plot_histogram(x,gray,'race.tif','Histogram_race',L)
	im = Image.open ('kids.tif')
	x = np.array(im)
	plot_histogram(x,gray,'kids.tif','Histogram_kids',L)
##########   Section 2  ###########################################
def CDF(H):
	#cdf
	Fx = []
	for i in range(0,len(H)):
		sum = 0
		for j in range(0,i+1):
			sum += H[j]
		Fx.append(sum)
	return Fx
def equalize(H,X,L):
	#X	= Image array
	#H	= Histogram of X
	H_norm = 0
	for i in range(0,len(H)):
		H_norm += H[i]

	x = (np.reshape(X,[1,np.prod(X.shape)])).squeeze()
	z = np.zeros(x.shape)


	for i in range(0,len(x)):
		num=0
		for j in range(0,x[i]+1):
			num += H[j]
		Ys = num/H_norm
		Ymax, Ymin = 1,0
		Zs = (L-1)*(Ys - Ymin)/(Ymax-Ymin)
		z[i] = Zs
	return z
def section_2():
	L=256
	name='kids.tif'
	gray = cm.get_cmap('gray', L)
	im = Image.open(name)
	X = np.array(im)
	H,_ = np.histogram(X.flatten(),L,[0,L])
	Z = equalize(H,X,L)
	Fx = CDF(H)
	Z = np.reshape(Z,X.shape)
	plot_histogram(Z,gray,name,'Hist_equalized_'+name.split('.')[0],L)


	plt.figure()
	plt.plot(np.array(Fx)*np.max(H)/np.max(Fx))
	plt.title('Cumulative Distribution of Image')
	plt.hist(X.flatten(),bins=np.linspace(0,255,L))
	plt.legend(['Normalized CDF','Histogram'])
	plt.savefig('Normalized_Fx_'+name.split('.')[0]+'.png')
	plt.savefig('Normalized_Fx_'+name.split('.')[0]+'.tif')

	plt.figure()
	plt.plot(np.array(Fx)/np.max(Fx))
	plt.title('Cumulative Distribution of Image')
	plt.savefig('Fx_'+name.split('.')[0]+'.png')
	plt.savefig('Fx_'+name.split('.')[0]+'.tif')


	# Equalization Comparison with opencv implementation
	img_eq = cv2.equalizeHist(X)
	plt.figure(figsize=(10,15))
	plt.subplot(231)
	plt.imshow(Z,cmap=plt.cm.gray)
	plt.title('Custom')
	plt.subplot(232)
	plt.imshow(img_eq,cmap=plt.cm.gray)
	plt.title('Opencv')
	error = img_eq-Z
	plt.subplot(233)
	plt.imshow(error,cmap=plt.cm.gray)
	plt.title('Error Between Them')
	plt.subplot(234)
	plt.hist(Z.flatten(),bins=np.linspace(0,255,L))
	plt.subplot(235)
	plt.hist(img_eq.flatten(),bins=np.linspace(0,255,L), color = 'r')
	plt.subplot(236)
	plt.hist(error.flatten(),bins=np.linspace(0,255,L), color = 'r')
	plt.savefig('Comparison between Implementations_'+name.split('.')[0]+'.png')

	img_out = Image.fromarray(Z.astype(np.uint8))
	img_out.save('equalized_'+name.split('.')[0]+'.tif')
##########   Section 3  ###########################################
def stretch(input,T1,T2):
	input = np.where(input<=T1,0,input)
	input = np.where(input>=T2,255,input)
	input = np.where((input>T1)&(input<T2),(255/(T2-T1))*(input-T1),input)
	return input
def section_3():
	L=256
	name='kids.tif'
	T1 = 70
	T2 = 180
	gray = cm.get_cmap('gray', L)
	im = Image.open(name)
	X = np.array(im)
	im_out = stretch(X,T1,T2)
	plt.figure(figsize=(10,10))
	plt.subplot(221)
	plt.imshow(X,cmap=gray)
	plt.title('Input Image')
	plt.subplot(222)
	plt.imshow(im_out,cmap=gray)
	plt.title('Stretched Image')
	plt.subplot(223)
	plt.hist(X.flatten(),bins=np.linspace(0,255,L))
	plt.title('Histogram of Input Image')
	plt.subplot(224)
	plt.hist(im_out.flatten(),bins=np.linspace(0,255,L))
	plt.title('Histogram of Stretched Image')
	plt.savefig('Image_Stretch.png')
	plt.savefig('Image_Stretch.tif')
###################################################################
def construct_pattern(stripe_height=16,img_size=[256,256],gray_level=256):
	checkerboard_pattern = np.array([[255,255,0,0],[255,255,0,0],[0,0,255,255],[0,0,255,255]])
	A = np.ones((img_size[1],img_size[0]))*gray_level
	for i in range(0,img_size[1],32):
		row_start = i
		row_end = i+stripe_height
		col_start = 0
		col_end = img_size[0]
		for r in range(row_start,row_end,4):
			for c in range(col_start,col_end,4):
				A[r:r+4,c:c+4] = checkerboard_pattern
	plt.figure()
	plt.imshow(A,cmap=cm.get_cmap('gray', 256))
	plt.title('Gray Level = '+str(gray_level))
	plt.show()
	img_out = Image.fromarray(A.astype(np.uint8))
	img_out.save('pattern.tif')
	print("\n\nThe pattern is saved as 'pattern.tif' in the current directory\n\n")
def gamma_correction(gamma,img_name):
	gray = cm.get_cmap('gray', 256)
	im = Image.open (img_name)
	x = np.array(im)
	gamma_corrected_image = np.power((x/255),1/gamma)*255
	plt.figure()
	plt.imshow(x,cmap=gray)
	plt.title(img_name)
	plt.savefig('linear_image.tif')
	plt.figure()
	plt.imshow(gamma_corrected_image,cmap=gray)
	plt.title('Gamma Corrected '+img_name)
	plt.savefig('Gamma_Corrected_1.tif')
	return gamma_corrected_image
def gamma_correction_2(gamma,img_name):
	gray = cm.get_cmap('gray', 256)
	im = Image.open (img_name)
	x = np.array(im)
	gamma_corrected_image = np.power((x/255),gamma/1.5)*255
	plt.figure()
	plt.imshow(x,cmap=gray)
	plt.title(img_name)
	plt.savefig('Gamma_15 Image.tif')
	plt.figure()
	plt.imshow(gamma_corrected_image,cmap=gray)
	plt.title('Gamma Corrected '+img_name)
	plt.savefig('Gamma_Coorected_gamma_15.tif')
	return gamma_corrected_image
def section_4():
	stripe_height=16
	img_size=[256,256]
	gray = 130#Best intensity match while looked at the image from distance
	construct_pattern(stripe_height=stripe_height,img_size=img_size,gray_level=gray)
	calculated_gamma = 1.028821801
	gamma_corrected_image = gamma_correction(calculated_gamma,'linear.tif')
	img_out = Image.fromarray(gamma_corrected_image.astype(np.uint8))
	img_out.save('gamma_corrected_image.tif')

	gamma_corrected_image = gamma_correction_2(calculated_gamma,'gamma15.tif')
	img_out = Image.fromarray(gamma_corrected_image.astype(np.uint8))
	img_out.save('gamma_corrected_image_2.tif')

###################################################################
def Main():
	#section_1()
	#section_2()
	#section_3()
	section_4()
Main()
