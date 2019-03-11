import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import edgemasking as em
import cv2


hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data


imageslice = image
imageslice =  em.backgroundremoval(imageslice,3421)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(imageslice,kernel,iterations = 1)
closing = cv2.morphologyEx(imageslice, cv2.MORPH_CLOSE, kernel)
edges = em.auto_canny(np.uint8(closing),0.01)


plt.subplot(121),plt.imshow(imageslice,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()