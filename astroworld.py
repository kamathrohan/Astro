import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt
import edgemasking as em


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

edges_1 = em.sourcedetection(region_1)
edges_2 = em.sourcedetection(region_2)
edges_3 = em.sourcedetection(region_3)
edges_4 = em.sourcedetection(region_4)

plt.imshow(region_3)
plt.show()
plt.imshow(edges_3)
plt.show()
