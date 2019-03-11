import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits



def edgemasking(data,xstart,xend,ystart,yend):
    """
    :param data: image whose edges need to be masked
    :param xstart: starting value of edges (x axis)
    :param xend:  last value of edges (x axis)
    :param ystart: starting values of edges (y axis)
    :param yend: last value of edges (x axis)
    :return: masked image
    """
    for i in range(xstart,xend):
        for j in range(ystart,yend):
            data[i][j] = 0
    return data
