import numpy as np
import cv2
import matplotlib.pyplot as plt
from astropy.io import fits
import edgemasking as em


hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data

for i in image:
    for j in i:
        if j > 4000:
            j = 0
