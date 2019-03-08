import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt





hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data
image_info = hdulist.info()
img = cv2.imread("galaxies.jpeg")

print(img)
kernel = (1/25)*np.array([[0,0,0,0,0],[0,0,0,0,0],[5,5,5,5,5],[0,0,0,0,0],[0,0,0,0,0]])
dst = cv2.filter2D(img,-1,kernel)


<<<<<<< HEAD
=======

edges = cv2.Canny(dst,0,5)

>>>>>>> 597a47b75c3c24586a46d910791dfbfd12552dee
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edgecks([]), plt.yticks([])

plt.show()s,cmap = 'gray')
plt.title('Edge Image'), plt.xti