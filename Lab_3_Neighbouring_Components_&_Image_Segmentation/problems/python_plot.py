import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse

parser = argparse.ArgumentParser(description='Image Segmentation',
					usage='Segmenting a Gray Scale Image',
					epilog='Give proper arguments')
parser.add_argument('-T',"--threshold",metavar='',help="Threshold value for neighbourhood segmentation")

args = parser.parse_args()

threshold=args.threshold


# Read in a segmentation TIFF image.
im = Image.open('./output/segmentation_'+str(threshold)+'.tif')
# Import Image Data into Numpy array.
x = np.array(im)
# Obtain number of segmentation area.
N = np.max(x)
# Randomly set color map.
cmap = mpl.colors.ListedColormap(np.random.rand(N+1 ,3))
plt.imshow(x,cmap=cmap,interpolation='none')
plt.colorbar()
plt.title('Segmented Image, Threshold = '+str(threshold))
#plt.show()
plt.savefig('./output/segmented_image_plot_'+str(threshold)+'.tif')
plt.savefig('./output/segmented_image_plot_'+str(threshold)+'.png')
