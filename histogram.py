import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import edgemasking as em
import scipy.ndimage.morphology as sp

hdulist = fits.open("A1_mosaic.fits")
image = hdulist[0].data

newimage = em.edgemasking(image,0,4611,0,100)
newimage = em.edgemasking(newimage,0,4611,2470,2570)
newimage = em.edgemasking(newimage,4511,4611,0,2570)


numbers = []
for i in newimage:
    for j in i:
        numbers.append(j)

plt.hist(numbers, bins=range(0, max(numbers) + 5, 5))
plt.xlabel("Pixel Value")
plt.ylabel("Number of Pixels")
plt.yscale('log')
plt.show()