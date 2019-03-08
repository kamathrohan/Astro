import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em
import skimage






hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data

em.edgemasking(image,0,4611,0,100)
em.edgemasking(image,0,4611,2470,2570)
em.edgemasking(image,4511,4611,0,2570)


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
#kernel = cv2.getGaussianKernel(50,1)
erosion = cv2.erode(image,kernel,iterations = 5)
erosion = np.uint8(erosion)
edges = cv2.Canny(erosion,200,300)

plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(erosion,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
