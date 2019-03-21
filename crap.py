import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology as sp

hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data

imageslice = image[100:500,200:400]
plt.imshow(imageslice)
plt.show()
print(em.fluxarray(imageslice, Rohan = True,im_show=True))
