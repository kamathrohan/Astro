import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology as sp

hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data
imageslice = image[200:500,200:300]


print(em.fluxarray(imageslice, Rohan = True))

plt.imshow(imageslice)
plt.show()