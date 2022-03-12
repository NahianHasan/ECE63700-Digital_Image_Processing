import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from PIL import Image

def section_2_3(data):
	print('\n\n\n############# Section 2-3 ##################')
	######################## Section 2 ##############################
	# List keys of dataset
	print(data.keys())
	x0 = data['x'][0]
	y0 = data['y'][0]
	z0 = data['z'][0]
	plt.figure(figsize=(10,10))
	plt.plot(x0, linewidth=4)
	plt.plot(y0, linewidth=4)
	plt.plot(z0, linewidth=4)
	plt.legend([r'$x_0$',r'$y_0$',r'$z_0$'],fontsize=15)
	plt.xticks(range(0,31,1),range(400,710,10),rotation=90,fontsize=15)
	plt.yticks(fontsize=15)
	plt.xlabel('Wavelength,'+r'$\lambda$'+'(nm)',fontsize=20)
	plt.ylabel('color matching functions',fontsize=20)
	plt.savefig('color_matching_function.tif')
	plt.savefig('color_matching_function.png')

	A_inv = np.array([[0.2430,0.8560,-0.0440],[-0.3910,1.1650,0.0870],[0.0100,-0.0080,0.5630]])
	T = np.array([[x0],[y0],[z0]])
	T = np.reshape(T,[T.shape[0],T.shape[-1]])
	print('T = ',T.shape)
	print('A_inv = ',A_inv.shape)
	CMF = np.matmul(A_inv,T)
	print('CMF = ',CMF.shape)
	plt.figure(figsize=(10,10))
	plt.plot(CMF[0,:], linewidth=4)
	plt.plot(CMF[1,:], linewidth=4)
	plt.plot(CMF[2,:], linewidth=4)
	plt.legend([r'$l_0$',r'$m_0$',r'$s_0$'],fontsize=15)
	plt.xticks(range(0,31,1),range(400,710,10),rotation=90,fontsize=15)
	plt.yticks(np.divide(range(0,11,1),100),fontsize=15)
	plt.xlabel('Wavelength,'+r'$\lambda$'+'(nm)',fontsize=20)
	plt.ylabel('color matching functions',fontsize=20)
	plt.savefig('CMF.tif')
	plt.savefig('CMF.png')

	D_65 = data['illum1'][0]
	flour = data['illum2'][0]
	plt.figure(figsize=(10,10))
	plt.plot(D_65, linewidth=4)
	plt.plot(flour, linewidth=4)
	plt.legend([r'$D_{65}$','Fluorescent'],fontsize=15)
	plt.xticks(range(0,31,1),range(400,710,10),rotation=90,fontsize=15)
	plt.xlabel('Wavelength,'+r'$\lambda$'+'(nm)',fontsize=20)
	plt.yticks(fontsize=15)
	plt.ylabel('Spectrum',fontsize=20)
	plt.savefig('Spectrum.tif')
	plt.savefig('Spectrum.png')

	########################## Section 3 ###############################
	S = np.sum(T,axis=0)
	S = np.reshape(S,[1,S.shape[0]])
	print('S = ',S.shape)
	x,y,z = x0/S,y0/S,z0/S
	x,y,z = x.T,y.T,z.T
	print('x = ',x.shape)
	print('y = ',y.shape)
	print('z = ',z.shape)
	#D_65 primaries
	R = [0.73467, 0.26533, 0.0]
	G = [0.27376, 0.71741, 0.00883]
	B = [0.16658, 0.00886, 0.82456]
	x_w,y_w,z_w = 0.3127, 0.3290, 0.3583#D_65 white point
	x_e,y_e,z_e = 0.3333, 0.3333, 0.3333#Equal energy white point
	plt.figure(figsize=(10,10))
	plt.plot(x,y, linewidth=4)
	plt.xlabel('X',fontsize=20)
	plt.yticks(fontsize=15)
	plt.ylabel('Y',fontsize=20)
	plt.title("Chromaticity Diagram (as a function of "+r'$\lambda$'+")",fontsize=15)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=15)
	L = 400
	for xt,yt in zip(x,y):
		label = r'$\lambda=$'+str(L)
		plt.annotate(label, # this is the text
					(xt,yt), # these are the coordinates to position the label
					textcoords="offset points", # how to position the text
					xytext=(10,0), # distance from text to points (x,y)
					ha='center',
					fontsize=15) # horizontal alignment can be left, right or center
		L += 10

	plt.savefig('Chromaticity.png')
	plt.savefig('Chromaticity.tif')


	plt.figure(figsize=(10,10))
	plt.plot(x,y, linewidth=4, label='Chromaticity diagram')
	plt.plot(R[0],R[1],marker="o", markersize=15, markeredgecolor="red", markerfacecolor="red", label='D_65_Red_Primary')
	plt.plot(G[0],G[1],marker="o", markersize=15, markeredgecolor="green", markerfacecolor="green", label='D_65_Green_Primary')
	plt.plot(B[0],B[1],marker="o", markersize=15, markeredgecolor="blue", markerfacecolor="blue", label='D_65_Blue_Primary')
	plt.plot([R[0],G[0]],[R[1],G[1]], linewidth=4)
	plt.plot([R[0],B[0]],[R[1],B[1]], linewidth=4)
	plt.plot([B[0],G[0]],[B[1],G[1]], linewidth=4)
	plt.plot(x_w,y_w, marker="o", markersize=15, markeredgecolor="Black", markerfacecolor="Black", label='D_65_white_point')
	plt.plot(x_e,y_e, marker="o", markersize=15, markeredgecolor="Grey", markerfacecolor="Grey", label='Equal_energy_white_point')

	plt.xlabel('X',fontsize=20)
	plt.yticks(fontsize=15)
	plt.ylabel('Y',fontsize=20)
	plt.title("Chromaticity Diagram (D_65) (as a function of "+r'$\lambda$'+")",fontsize=15)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=15)
	plt.annotate('R',(R[0],R[1]),textcoords="offset points",xytext=(10,10),ha='center',fontsize=20)
	plt.annotate('G',(G[0],G[1]),textcoords="offset points",xytext=(10,10),ha='center',fontsize=20)
	plt.annotate('B',(B[0],B[1]),textcoords="offset points",xytext=(10,10),ha='center',fontsize=20)
	plt.legend()
	plt.savefig('Chromaticity_Combined_D_65.png')
	plt.savefig('Chromaticity_Combined_D_65.tif')
	#Rec. 709RGB primaries
	R = [0.640, 0.330, 0.030]
	G = [0.300, 0.600, 0.100]
	B = [0.150, 0.060, 0.790]
	plt.figure(figsize=(10,10))
	plt.plot(x,y, linewidth=4, label='Chromaticity diagram')
	plt.plot(R[0],R[1],marker="o", markersize=15, markeredgecolor="red", markerfacecolor="red", label='Rec_709_RGB_Red_Primary')
	plt.plot(G[0],G[1],marker="o", markersize=15, markeredgecolor="green", markerfacecolor="green", label='Rec_709_RGB_Green_Primary')
	plt.plot(B[0],B[1],marker="o", markersize=15, markeredgecolor="blue", markerfacecolor="blue", label='Rec_709_RGB_Blue_Primary')
	plt.plot([R[0],G[0]],[R[1],G[1]], linewidth=4)
	plt.plot([R[0],B[0]],[R[1],B[1]], linewidth=4)
	plt.plot([B[0],G[0]],[B[1],G[1]], linewidth=4)
	plt.plot(x_w,y_w, marker="o", markersize=15, markeredgecolor="Black", markerfacecolor="Black", label='D_65_white_point')
	plt.plot(x_e,y_e, marker="o", markersize=15, markeredgecolor="Grey", markerfacecolor="Grey", label='Equal_energy_white_point')
	plt.legend()

	plt.xlabel('X',fontsize=20)
	plt.yticks(fontsize=15)
	plt.ylabel('Y',fontsize=20)
	plt.title("Chromaticity Diagram (Rec. 709 RGB) (as a function of "+r'$\lambda$'+")",fontsize=15)
	plt.xticks(fontsize=15)
	plt.yticks(fontsize=15)
	plt.annotate('R',(R[0],R[1]),textcoords="offset points",xytext=(10,10),ha='center',fontsize=20)
	plt.annotate('G',(G[0],G[1]),textcoords="offset points",xytext=(10,10),ha='center',fontsize=20)
	plt.annotate('B',(B[0],B[1]),textcoords="offset points",xytext=(10,10),ha='center',fontsize=20)
	plt.savefig('Chromaticity_Combined_709.png')
	plt.savefig('Chromaticity_Combined_709.tif')

##################### Section 4 ###############################
def gamma_correction(gamma,img):
	gamma_corrected_image = np.power((img/255),1/gamma)*255
	return gamma_corrected_image

def section_4(illuminant,name,T):
	print('\n\n\n############# Section 4 ##################')
	data = np.load('./reflect.npy',allow_pickle=True)[()]
	R = data['R']
	print('R = ',R.shape)
	print(name,' = ',illuminant.shape)
	I = np.zeros(R.shape)
	for i in range(0,R.shape[0]):
		for j in range(0,R.shape[1]):
			I[i,j,:] = np.multiply(R[i,j,:],illuminant)
	print('I = ',I.shape)
	XYZ = np.zeros((I.shape[0],I.shape[1],T.shape[0]))
	for i in range(0,I.shape[0]):
		for j in range(0,I.shape[1]):
			XYZ[i,j,:] = np.reshape(np.matmul(T,np.reshape(I[i,j,:],[I[i,j,:].shape[0],1])), [T.shape[0]])
	print('tristimulus = ',XYZ.shape)
	#Rec. 709RGB primaries
	R = [0.640, 0.330, 0.030]
	G = [0.300, 0.600, 0.100]
	B = [0.150, 0.060, 0.790]
	W = np.array([R,G,B]).T
	x_w,y_w,z_w = 0.3127, 0.3290, 0.3583#D_65 white point
	Q = np.array([x_w/y_w,1,z_w/y_w])
	Q = np.reshape(Q,[Q.shape[0],1])
	print('W = ',W.shape)
	print('Q = ',Q.shape)
	co_eff = np.matmul(np.linalg.inv(W),Q)
	print('Scaling Coefficients = ',co_eff.shape)
	M = np.matmul(W,np.diag((co_eff.squeeze())))
	print('M_'+name+' = ',M.shape)
	print('M_'+name+' = ',M)
	RGB = np.zeros(XYZ.shape)
	for i in range(0,XYZ.shape[0]):
		for j in range(0,XYZ.shape[1]):
			RGB[i,j,:] = np.reshape(np.matmul(np.linalg.inv(M),np.reshape(XYZ[i,j,:],[XYZ.shape[-1],1])),[XYZ.shape[-1]])
	print('RGB = ',RGB.shape)
	RGB = np.where(RGB<0,0,RGB)
	RGB = np.where(RGB>1,1,RGB)
	RGB = RGB*255#Scaling
	gamma_corrected_image = gamma_correction(2.2,RGB)
	img_out = Image.fromarray(gamma_corrected_image.astype(np.uint8))
	img_out.save('gamma_corrected_image_'+name+'.tif')

################### Section 5 ############################
def section_5():
	print('\n\n\n############# Section 5 ##################')
	x,s = np.linspace(0, 1, int(np.ceil(1/0.005)), retstep=True)
	y,s = np.linspace(0, 1, int(np.ceil(1/0.005)), retstep=True)
	#Rec. 709RGB primaries
	R = [0.640, 0.330, 0.030]
	G = [0.300, 0.600, 0.100]
	B = [0.150, 0.060, 0.790]
	W = np.array([R,G,B]).T
	co_eff = np.diag(np.array([1,1,1]))
	M = np.matmul(W,co_eff)
	print('M = ',M)
	RGB = np.zeros((x.shape[0],y.shape[0],3))
	for i in range(y.shape[0]):
		for j in range(0,x.shape[0]):
			RGB[i,j,:] = np.reshape(np.matmul(np.linalg.inv(M),np.reshape(np.array([x[j],y[i],1-x[j]-y[i]]),[3,1])),[3])

	print('RGB = ',RGB.shape)
	for i in range(RGB.shape[0]):
		for j in range(0,RGB.shape[1]):
			if (RGB[i,j,0] < 0 or RGB[i,j,1] < 0 or RGB[i,j,2] < 0):
				RGB[i,j,:] = np.array([1,1,1])

	RGB = RGB * 255
	gamma_corrected_image = gamma_correction(2.2,RGB)
	plt.figure(figsize=(10,10))
	plt.imshow((np.flip(gamma_corrected_image,axis=0)).astype(np.uint8),extent=[0,1,0,1])
	plt.plot(R[0],R[1],marker="o", markersize=15, markeredgecolor="red", markerfacecolor="red", label='Rec_709_RGB_Red_Primary')
	plt.plot(G[0],G[1],marker="o", markersize=15, markeredgecolor="green", markerfacecolor="green", label='Rec_709_RGB_Green_Primary')
	plt.plot(B[0],B[1],marker="o", markersize=15, markeredgecolor="blue", markerfacecolor="blue", label='Rec_709_RGB_Blue_Primary')
	plt.xlabel('X',fontsize=20)
	plt.yticks(fontsize=15)
	plt.ylabel('Y',fontsize=20)
	plt.xticks(fontsize=15)
	plt.legend()
	plt.savefig('chromaticity_section_5.tif')

def Main():
	# Load data.npy
	data = np.load('./CIE_data/data.npy',allow_pickle=True)[()]
	x0 = data['x'][0]
	y0 = data['y'][0]
	z0 = data['z'][0]
	D_65 = data['illum1'][0]
	flour = data['illum2'][0]
	T = np.array([[x0],[y0],[z0]])
	T = np.reshape(T,[T.shape[0],T.shape[-1]])

	section_2_3(data)
	section_4(D_65,'D_65',T)
	section_4(flour,'fluorescent',T)
	section_5()

Main()
