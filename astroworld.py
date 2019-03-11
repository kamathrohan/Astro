import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em
import skimage






hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data
newimage = em.backgrounddetection(image,4000)



newimage = em.edgemasking(newimage,0,4611,0,100)
newimage = em.edgemasking(newimage,0,4611,2470,2570)
newimage = em.edgemasking(newimage,4511,4611,0,2570)


edges = cv2.Canny(np.uint8(newimage),0,5000)

plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()



