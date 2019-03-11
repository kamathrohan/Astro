import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import edgemasking as em
import cv2


hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data
imageslice = image[2900:3500,1200:1700]

imageslice =  em.backgroundremoval(imageslice,3421)
kernel = np.ones((5,5),np.uint8)
#erosion = cv2.erode(np.uint8(imageslice),kernel,iterations = 1)
closing = cv2.morphologyEx(imageslice, cv2.MORPH_CLOSE, kernel)
edges = em.auto_canny(np.uint8(closing),0.01)
print(edges)


plt.subplot(121),plt.imshow(imageslice)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges)
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()

