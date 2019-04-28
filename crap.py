import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from utils import *
import scipy.ndimage.morphology as sp
from matplotlib.colors import LogNorm
import csv
import pandas as pd
from scipy.optimize import curve_fit

hdulist = fits.open("A1_mosaic.fits")
magzpt = hdulist[0].header['MAGZPT']
magzrr = hdulist[0].header ['MAGZRR']
image = hdulist[0].data

def linfit(x,a,b):
    return( a*x + b)

"""
fluxmaster = []
for i in range(100,1500,200):
    imageslice = image[100:300, i:i+200]
    fluxarray = em.fluxarray(imageslice, Rohan=True, im_show=True)
    for j in fluxarray:
        fluxmaster.append(j)
print(fluxmaster)

"""
d1 = pd.read_csv("catalogue.csv")
mags = (d1["22.914393726401688"]).tolist()

mags.append(22.914393726401688)
mags.sort()

x = []
y = []

for j in range(9,25):
    for i in range(len(mags)):
        if mags[i] > j:
            x.append(j)
            y.append(i)
            break

logy = np.log10(y)
print(logy)
yerr = []

popt,pcov = curve_fit(linfit,x[0:9],logy[0:9])
print(popt)

"""

for i in y:
    yerr.append(2*np.sqrt(i))
print(yerr)

fig = plt.figure()
ax = plt.axes()
ax.set_yscale("log")
ax.errorbar(x,y,yerr=yerr, fmt = 'r')
plt.show()

"""


