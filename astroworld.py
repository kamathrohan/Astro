import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
#import skimage as sk





hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data
hist = np.sum(image, axis = 0)
print(np.argmax(hist))
img = cv2.imread("galaxies.jpeg")


x, y = np.mgrid[:image.shape[0], :image.shape[1]]

print(x,y)


kernel = (1/25)*np.array([[0,0,0,0,0],[0,0,0,0,0],[5,5,5,5,5],[0,0,0,0,0],[0,0,0,0,0]])

edges = cv2.Canny(img,50,np.inf)





plt.plot(hist)
plt.title('Histogram')
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
