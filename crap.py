import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology as sp

hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data

edges = em.sourcedetection(image[200:300,200:300])
filled = sp.binary_fill_holes(edges)
plt.imshow(filled)
plt.show()