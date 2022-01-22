import os
import matplotlib.pyplot as plt
from PIL import Image


plt.figure(figsize=(20,20))
plt.subplot(141)
im = Image.open('./imgblur.tif')
plt.imshow(im)
plt.title('Blurred Image')
plt.subplot(142)
im = Image.open('./output/sharpened_image_0.2.tif')
plt.imshow(im)
plt.title('Sharpened Image (lambda=0.2)')
plt.subplot(143)
im = Image.open('./output/sharpened_image_0.8.tif')
plt.imshow(im)
plt.title('Sharpened Image (lambda=0.8)')
plt.subplot(144)
im = Image.open('./output/sharpened_image_1.5.tif')
plt.imshow(im)
plt.title('Sharpened Image (lambda=1.5)')
plt.tight_layout()
plt.savefig('./output/Sharpening_Comparison.png')
plt.savefig('./output/Sharpening_Comparison.tif')
#plt.show()
