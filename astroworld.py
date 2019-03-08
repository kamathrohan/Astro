import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
<<<<<<< HEAD
#import skimage as sk
=======
import edgemasking as em
import skimage

>>>>>>> 0e0b9fb91e2157e6b055475e6478a9f029938007





hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data
<<<<<<< HEAD
hist = np.sum(image, axis = 0)
print(np.argmax(hist))
img = cv2.imread("galaxies.jpeg")


x, y = np.mgrid[:image.shape[0], :image.shape[1]]

print(x,y)


kernel = (1/25)*np.array([[0,0,0,0,0],[0,0,0,0,0],[5,5,5,5,5],[0,0,0,0,0],[0,0,0,0,0]])

edges = cv2.Canny(img,50,np.inf)
=======

em.edgemasking(image,0,4611,0,100)
em.edgemasking(image,0,4611,2470,2570)
em.edgemasking(image,4511,4611,0,2570)


kernel = (1/25)*np.array([[0,0,0,0,0],[0,0,0,0,0],[5,5,5,5,5],[0,0,0,0,0],[0,0,0,0,0]])
dst = cv2.GaussianBlur(img, (5,5),0)
dst = cv2.filter2D(image,-1,kernel)
>>>>>>> 0e0b9fb91e2157e6b055475e6478a9f029938007




<<<<<<< HEAD

plt.plot(hist)
plt.title('Histogram')
plt.subplot(121),plt.imshow(img,cmap = 'gray')
=======
plt.subplot(121),plt.imshow(image,cmap = 'gray')
>>>>>>> 0e0b9fb91e2157e6b055475e6478a9f029938007
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
