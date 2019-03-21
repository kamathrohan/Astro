import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology as sp

hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data
"""
fluxmaster = []
for i in range(100,1500,200):
    imageslice = image[100:300, i:i+200]
    fluxarray = em.fluxarray(imageslice, Rohan=True, im_show=True)
    for j in fluxarray:
        fluxmaster.append(j)
print(fluxmaster)

"""



imageslice = image[100:1000,100:1000]
plt.imshow(imageslice)
plt.show()
print(em.fluxarray(imageslice, Rohan = True,im_show=True))




