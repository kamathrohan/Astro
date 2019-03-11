import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em





hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data


print(image.shape)
#newimage = em.backgrounddetection(image,3421)

#random data split
data_split = image[300:600,300:600]



#Edges removal
newimage= em.backgrounddetection(image, 3421)
plt.imshow(newimage)
plt.show()


newimage = em.edgemasking(newimage,0,4611,0,100)
newimage = em.edgemasking(newimage,0,4611,2470,2570)
newimage = em.edgemasking(newimage,4511,4611,0,2570)


#log correction
#img = em.logcorrected(np.uint8(newimage))

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
#erosion = cv2.erode(image, kernel, iterations = 1)
edges = em.auto_canny(np.uint8(newimage))



#plt.plot(hist)
#plt.title('Histogram')
plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
