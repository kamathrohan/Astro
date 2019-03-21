import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology as sp

hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data




numbers = []
for i in image:
    for j in i:
        numbers.append(j)

plt.hist(numbers, bins=range(0, max(numbers) + 1000, 1000))
plt.xlabel("Pixel Value")
plt.ylabel("Number of Pixels")
plt.yscale('log')
plt.show()