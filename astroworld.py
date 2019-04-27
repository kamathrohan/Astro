from utils import *
import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import scipy.ndimage.morphology as sp

#print entire arrays
np.set_printoptions(threshold=np.nan)


# Le file avec le image
hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data
magzpt = hdulist[0].header['MAGZPT']
magzrr = hdulist[0].header ['MAGZRR']


#mask actual edges of image lol
newimage = masking(image,0,0,0,4611,0,100)
newimage = masking(newimage,0,0,0,4611,2470,2570)
newimage = masking(newimage,0,0,4511,4611,0,2570)

"""
==========================================================================================================
Preprocessing: Masking Region 1 (main star and main star diffraction)
==========================================================================================================
"""
region_1 = newimage[3150:3300, 1350:1550]
edges_1 = sourcedetection(region_1)
smooth = 255*sp.binary_fill_holes(edges_1, structure = np.ones((3,3))).astype(int)
smooth_region1 = np.uint8(smooth)
rsx, rex, rsy, rey = contour_coordinates(smooth_region1, all = True, im_show = False)
mask_1 = masking(newimage, 3150, 1350, rsy, rey, rsx, rex, a_lot  = True)

"""
==========================================================================================================
Preprocessing: Masking Region 2 (bleeding line from main star)
==========================================================================================================
"""

region_2 = newimage[0:4611, 1150:1600]
edges_2 = sourcedetection(region_2)
smooth = 255*sp.binary_fill_holes(edges_2, structure = np.ones((2,2))).astype(int)
smooth_region2 = np.uint8(smooth)
rsx, rex, rsy, rey = contour_coordinates(smooth_region2,  all = True , im_show = False)
mask_2 = masking(mask_1, 0, 1150, rsy, rey, rsx, rex, a_lot  = True)


"""
==========================================================================================================
Preprocessing: Masking Region 3 (stars region 1, left under main star)
==========================================================================================================
"""
region_3 = newimage[2100:2450, 600:1100]
edges_3 = sourcedetection(region_3)
smooth = 255*sp.binary_fill_holes(edges_3, structure = np.ones((2,2))).astype(int)
smooth_region3 = np.uint8(smooth)
rsx,rex,rsy,rey = contour_coordinates(smooth_region3, all = True, im_show= False)
mask_3 = masking(mask_2, 2100, 600, rsy, rey, rsx, rex, a_lot  = True)



"""
==========================================================================================================
Preprocessing: Masking Region 4
==========================================================================================================
"""
region_4 = newimage[3000:3900, 2100:2400]
edges_4 = sourcedetection(region_4)
smooth = 255*sp.binary_fill_holes(edges_4, structure = np.ones((2,2))).astype(int)
smooth_region4 = np.uint8(smooth)
rsx,rex,rsy,rey = contour_coordinates(smooth_region4, all = True, im_show= False)
mask_4 = masking(mask_3, 3000, 2100, rsy, rey, rsx, rex, a_lot = True)



"""
==========================================================================================================
Preprocessing: Masking Region 5
==========================================================================================================
"""
region_5 = newimage[3150:3450, 600:900]
edges_5 = sourcedetection(region_5)
smooth = 255*sp.binary_fill_holes(edges_5, structure = np.ones((2,2))).astype(int)
smooth_region5 = np.uint8(smooth)
rsx,rex,rsy,rey = contour_coordinates(smooth_region5, all = True, im_show = False)
mask_5 = masking(mask_4, 3150, 600, rsy, rey, rsx, rex, a_lot = True)

"""
==========================================================================================================
Preprocessing: Masking Region 6
==========================================================================================================
"""
region_6 = newimage[3369:3650, 1420:1450]
edges_6 = sourcedetection(region_6)
smooth = 255*sp.binary_fill_holes(edges_6, structure = np.ones((3,3))).astype(int)
smooth_region6 = np.uint8(smooth)
rsx,rex,rsy,rey = contour_coordinates(smooth_region5, all = False, im_show= False)
mask_6 = masking(mask_5, 3369, 1420, rsy, rey, rsx, rex, a_lot = True)



"""
==========================================================================================================
Preprocessing: Masking Region 7
==========================================================================================================
"""
region_7 = newimage[2700:2840, 950:990]
edges_7 = sourcedetection(region_7)
smooth = 255*sp.binary_fill_holes(edges_7, structure = np.ones((3,3))).astype(int)
smooth_region7 = np.uint8(smooth)
rsx,rex,rsy,rey = contour_coordinates(smooth_region5, all = True, im_show= False)
mask_7 = masking(mask_6, 2700, 950, rsy, rey, rsx, rex, a_lot = True)


np.savetxt("masked.txt",mask_7)
"""
fig, (ax1, ax2) = plt.subplots(1,2)

ax1.imshow(newimage)
ax1.set_title('Before Masking')
ax2.imshow(mask_7)
ax2.set_title('After Masking')
plt.show()
"""

"""
==========================================================================================================
Producing catalogue
==========================================================================================================
"""

flux, xstarts, xends, ystarts, yends, mags = catalogue(mask_7, magzpt)
print(mags)



"""
Useful websites:
https://www.programcreek.com/python/example/70455/cv2.drawContours
http://answers.opencv.org/question/120499/how-to-eliminate-small-contours-in-a-binary-image/
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.morphology.binary_fill_holes.html
"""
