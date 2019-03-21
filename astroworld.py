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
newimage = em.edgemasking(image,0,0,0,4611,0,100)
newimage = em.edgemasking(newimage,0,0,0,4611,2470,2570)
newimage = em.edgemasking(newimage,0,0,4511,4611,0,2570)

#data split by regions by interest
region_1 = newimage[2900:3500, 1200:1700] #main star and main star diffraction
region_2 = newimage[0:4611, 1410:1460] #bleeding line from main star
region_3 = newimage[2100:2450,600:1100] #stars region 1, left under main star
region_4 = newimage[3000:3900, 2100:2400] #stars region 2



edges_1 = em.sourcedetection(region_1)
edges_2 = em.sourcedetection(region_2)
edges_3 = em.sourcedetection(region_3)
edges_4 = em.sourcedetection(region_4)
#edges_random = np.uint8(em.sourcedetection(newimage[200:400,200:400], fill = True))


smooth = 255*sp.binary_fill_holes(edges_3, structure=np.ones((2,2))).astype(int)
smooth1_region3 = np.uint8(smooth)
rsx,rex,rsy,rey = em.contour_coordinates(smooth1_region3, all = False, im_show=False)

#mask1_region1  =
mask1_region3 = em.edgemasking(newimage, 2100, 600, rsy[0], rey[0], rsx[0], rex[0])

smooth = 255*sp.binary_fill_holes(edges_1, structure=np.ones((3,3))).astype(int)
smooth_region1 = np.uint8(smooth)
rsx, rex, rsy, rey = em.contour_coordinates(smooth_region1, all = True, im_show = True)


plt.imshow(edges_1)
plt.show()

"""

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax1.imshow(edges_3, cmap = 'gray')
ax2 = fig.add_subplot(2,2,2)
ax2.imshow(region_3)
ax3 = fig.add_subplot(2,2,3)
ax3.imshow(linda)
plt.show()
"""



"""
instrumental magnitude conversion
1) get coordinates of boxes
1) obtain counts within box
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
