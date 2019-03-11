import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from tqdm import tqdm
import cv2 as cv2



def edgemasking(data,xstart,xend,ystart,yend):
    """
    :param data: image whose edges need to be masked
    :param xstart: starting value of edges (x axis)
    :param xend:  last value of edges (x axis)
    :param ystart: starting values of edges (y axis)
    :param yend: last value of edges (x axis)
    :return: masked image
    """
    array = np.copy(data)
    for i in tqdm(range(xstart,xend)):
        for j in tqdm(range(ystart,yend)):
            array[i][j] = 0
    return array


def backgrounddetection(data,threshold):
    """
    :param data: image whose background is to be removed (2D array)
    :param threshold: threshold below whoch something is the background
    :return:
    """
    image = np.copy(data)
    for i in tqdm(range(np.shape(image)[0])):
        for j in range(np.shape(image)[1]):
            if image[i][j] < threshold:
                image[i][j] = 0
    return image


def backgroundremoval(data,threshold):
    """
    :param data: image whose background is to be removed (2D array)
    :param threshold: threshold below whoch something is the background
    :return:
    """
    image = np.copy(data)
    for i in tqdm(range(np.shape(image)[0])):
        for j in range(np.shape(image)[1]):
            image[i][j]  = data[i][j] - threshold
    return image

def logcorrected(data):
    """
    :param data: image which is to be log corrected
    :return: log corrected image
    """
    image = np.copy(data)
    for i in tqdm(range(np.shape(image)[0])):
        for j in range(np.shape(image)[1]):
            if data[i][j] == 0 :
                image[i][j] = 0
            else:
                image[i][j] = np.log(data[i][j])
    return image


def auto_canny(image, sigma=0.33):
    """

    :param image:
    :param sigma:
    :return:
    """

    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(65536, (1.0 + sigma) * v))
    edges = cv2.Canny(image, lower, upper)
    return edges


def sourcedetection(image, threshold = 3421, sigma = 0.01):
    """

    :param image: image to find edges from
    :param threshold: background threshold to blanket subtract
    :param sigma: for autocanny
    :return:
    """
    imageslice = backgroundremoval(image, threshold)
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(imageslice, cv2.MORPH_CLOSE, kernel)
    edges = em.auto_canny(np.uint8(closing), sigma)

    return edges