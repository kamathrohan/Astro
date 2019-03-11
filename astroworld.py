import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em





hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data
newimage = em.backgrounddetection(image,4000)

print(image.shape)
data_split = image[300:600,300:600]

"""
plt.imshow(data_split)
plt.show()
"""


img = cv2.imread("galaxies.jpeg")

mask = em.edgemasking(image,0,4611,0,111)
#plt.imshow(mask)
#plt.show()



#Sobel filter



edges = cv2.Canny(img,75,np.inf)

newimage = em.edgemasking(newimage,0,4611,0,100)
newimage = em.edgemasking(newimage,0,4611,2470,2570)
newimage = em.edgemasking(newimage,4511,4611,0,2570)


edges = cv2.Canny(np.uint8(newimage),0,5000)

#plt.plot(hist)
#plt.title('Histogram')
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
