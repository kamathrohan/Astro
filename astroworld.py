import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em





hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data


print(image.shape)
newimage = em.backgrounddetection(image,4000)

#random data split
data_split = image[300:600,300:600]

"""
plt.imshow(data_split)
plt.show()
"""


mask = em.edgemasking(image,0,4611,0,111)
#plt.imshow(mask)
#plt.show()


#Edges removal

newimage = em.edgemasking(newimage,0,4611,0,100)
newimage = em.edgemasking(newimage,0,4611,2470,2570)
newimage = em.edgemasking(newimage,4511,4611,0,2570)


#background subtraction


corrected_image = em.backgrounddetection(newimage, 3421)


edges = cv2.Canny(np.uint8(corrected_image),100,500)


#plt.plot(hist)
#plt.title('Histogram')
plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
