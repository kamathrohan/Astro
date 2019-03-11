import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em


hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data


#print(image.shape)
newimage = em.backgroundremoval(image,3421)
plt.imshow(newimage)
plt.show()

#mask edges of image "region_3"
newimage = em.edgemasking(newimage,0,4611,0,100)
newimage = em.edgemasking(newimage,0,4611,2470,2570)
newimage = em.edgemasking(newimage,4511,4611,0,2570)

#data split by regions by interest
region_1 = newimage[2900:3500, 1200:1700] #main star and main star diffraction
region_2 = newimage[0:4611, 1410:1460] #bleeding line from main star
region_3 = newimage[2100:2450,600:1100] #stars region 1
region_4 = newimage[3000:3900, 2100:2400] #stars region 2





kernel = np.ones((5,5),np.uint8)
closing = cv2.morphologyEx(region_1, cv2.MORPH_CLOSE, kernel)
edges = em.auto_canny(np.uint8(closing), 0.01)
plt.imshow(edges)
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()


"""
#plt.plot(hist)
#plt.title('Histogram')
plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
"""
