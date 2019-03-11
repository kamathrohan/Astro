import numpy as np
import cv2
import matplotlib.pyplot as plt
from astropy.io import fits
import edgemasking as em


hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data

for i in image:
    for j in i:
        if j > 3421:
            j = 0
