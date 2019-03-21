import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology as sp


hdulist = fits.open("A1_mosaic.fits")
magzpt = hdulist[0].header['MAGZPT']
magzrr = hdulist[0].header ['MAGZRR']
image = hdulist[0].data
imageslice = image[200:400,200:300]
fluxarray = em.fluxarray(imageslice)
mags = em.magnitudes(fluxarray,magzpt)
print(mags)


plt.imshow(imageslice)
plt.show()
