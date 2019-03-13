import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology
np.set_printoptions(threshold=np.nan)

hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data

#mask edges of image "region_5"
newimage = em.edgemasking(image,0,4611,0,100)
newimage = em.edgemasking(newimage,0,4611,2470,2570)
newimage = em.edgemasking(newimage,4511,4611,0,2570)

#data split by regions by interest
region_1 = newimage[2900:3500, 1200:1700] #main star and main star diffraction
region_2 = newimage[0:4611, 1410:1460] #bleeding line from main star
region_3 = newimage[2100:2450,600:1100] #stars region 1
region_4 = newimage[3000:3900, 2100:2400] #stars region 2
"""

"""



edges_1 = em.sourcedetection(region_1)
edges_2 = em.sourcedetection(region_2)
edges_3 = em.sourcedetection(region_3)
edges_4 = em.sourcedetection(region_4)


"""
Obtaining contours and finding max contour by area and fitting to polygon
"""

contours, hierarchy = cv2.findContours(edges_3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#areas = [cv2.contourArea(c) for c in contours] # get the area of each contour
#min_index = np.argmin(areas) # get the index of the largest contour by area
cnts = contours
for c in range(len(cnts)):
    cnts = contours[c] # get the largest contour by area
    cv2.drawContours(edges_3, [cnts], 0, (0,255,0), 3) # Draw the contours to the mask image
    x,y,w,h = cv2.boundingRect(cnts) #  get the bouding box information about the contour
    cv2.rectangle(edges_3,(x,y),(x+w,y+h),(255,255,255),2) # Draw rectangle on the image to represent the bounding box
    cv2.imshow("debug.", edges_3)
    cv2.waitKey()

"""
Useful websites:
https://www.programcreek.com/python/example/70455/cv2.drawContours
http://answers.opencv.org/question/120499/how-to-eliminate-small-contours-in-a-binary-image/
https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.morphology.binary_fill_holes.html
"""
