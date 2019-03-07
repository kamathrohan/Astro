import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt



hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data
image_info = hdulist.info()
img = cv2.imread("galaxies.jpeg")
edges = cv2.Canny(img,0,np.inf)


print(image_info)


plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()

#def maskedges(xstart,xend,ystart,yend,image):
