import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

channel={'0':'red','1':'green','2':'blue'}
Im = Image.open('./img12.tif')
Im = np.array(Im)
plt.figure(figsize=(25,25))
filtered_image = np.zeros(Im.shape)
for ch in range(0,Im.shape[-1]):
	I = Im[:,:,ch]
	h = np.ones((I.shape),dtype=np.double)
	print(h.shape)
	for i in range(1,I.shape[0]):
		for j in range(1,I.shape[1]):
			h[i,j] = 0.01*I[i,j] + 0.9*(h[i-1,j]+h[i,j-1]) - 0.81*h[i-1,j-1]
	print(type(h),'--',np.max(h),'--',np.min(h))
	im_save = Image.fromarray((255*100*h).astype(np.uint8))
	im_save.save('./output/h_out_'+channel[str(ch)]+'.tif')
	filtered_image[:,:,ch] = h
	h = Image.fromarray(h)
	plt.subplot(230+ch+4)
	plt.imshow(h)
	plt.title('Filtered channel '+channel[str(ch)])
	
	
filtered_image = np.array(filtered_image)
filtered_image = Image.fromarray(filtered_image.astype(np.uint8))
filtered_image.save('./output/IIR_Filtered_Image_python.tif')
filtered_image.save('./output/IIR_Filtered_Image_python.png')
plt.subplot(231)
plt.imshow(Im)
plt.title('Original Image')
plt.subplot(232)
plt.imshow(filtered_image)
plt.title('Filtered Image')
plt.tight_layout()
plt.savefig('./output/Python_IIR_Filtered.png')
plt.savefig('./output/Python_IIR_Filtered.tif')

#plt.show()

