import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from utils import *
import scipy.ndimage.morphology as sp
from matplotlib.colors import LogNorm



hdulist = fits.open("A1_mosaic.fits")
magzpt = hdulist[0].header['MAGZPT']
magzrr = hdulist[0].header ['MAGZRR']
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

masked = image[700:900, 700:900]
plt.imshow(masked, norm = LogNorm())
plt.show()

flux, xstarts, xends, ystarts, yends, mags = catalogue(masked, magzpt, im_show=True)
print(mags)


with open()
