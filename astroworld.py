import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology as sp

np.set_printoptions(threshold=np.nan)

hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data
magzpt = hdulist[0].header['MAGZPT']
magzrr = hdulist[0].header ['MAGZRR']

#mask edges of image "region_5"
newimage = em.edgemasking(image,0,4611,0,100)
newimage = em.edgemasking(newimage,0,4611,2470,2570)
newimage = em.edgemasking(newimage,4511,4611,0,2570)

#data split by regions by interest
region_1 = newimage[2900:3500, 1200:1700] #main star and main star diffraction
region_2 = newimage[0:4611, 1410:1460] #bleeding line from main star
region_3 = newimage[2100:2450,600:1100] #stars region 1, left under main star
region_4 = newimage[3000:3900, 2100:2400] #stars region 2



edges_1 = em.sourcedetection(region_1)
edges_2 = em.sourcedetection(region_2)
edges_3 = em.sourcedetection(region_3)
edges_4 = em.sourcedetection(region_4)

kernel = np.ones((2,2))

smooth = 255*sp.binary_fill_holes(edges_3, structure = kernel).astype(int)
smooth_final = np.uint8(smooth)

#idex 202 is main star in region 3

rsx,rex,rsy,rey = em.contour_coordinates(smooth_final, all = False , im_show = False)


linda = em.edgemasking(region_3, rsy[0],rey[0], rsx[0], rex[0])



fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax1.imshow(edges_3, cmap = 'gray')
ax2 = fig.add_subplot(2,2,2)
ax2.imshow(region_3)
ax3 = fig.add_subplot(2,2,3)
ax3.imshow(linda)
plt.show()




"""
instrumental magnitude conversion
1) get coordinates of boxes
1) obtain counts whithin box
2) convert to magnitudes
"""
"""
# 1)
"""

"""
Useful websites:
https://www.programcreek.com/python/example/70455/cv2.drawContours
http://answers.opencv.org/question/120499/how-to-eliminate-small-contours-in-a-binary-image/
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.morphology.binary_fill_holes.html
"""
