import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from tqdm import tqdm
import cv2 as cv2
import scipy.ndimage.morphology as sp

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
    for i in range(xstart,xend):
        for j in range(ystart,yend):
            array[i][j] = 3421
    return array

def backgrounddetection(data,threshold):
    """
    :param data: image whose background is to be removed (2D array)
    :param threshold: threshold below whoch something is the background
    :return:
    """
    image = np.copy(data)
    for i in range(np.shape(image)[0]):
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
    for i in range(np.shape(image)[0]):
        for j in range(np.shape(image)[1]):
            image[i][j]  = data[i][j] - threshold
    return image

def logcorrected(data):
    """
    :param data: image which is to be log corrected
    :return: log corrected image
    """
    image = np.copy(data)
    for i in range(np.shape(image)[0]):
        for j in range(np.shape(image)[1]):
            if data[i][j] == 0 :
                image[i][j] = 0
            else:
                image[i][j] = np.log(data[i][j])
    return image

def auto_canny(image, sigma=0.01):
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

def sourcedetection(image, threshold = 3421, sigma = 0.33, fill = False):
    """
    :param image: image to find edges from
    :param threshold: background threshold to blanket subtract
    :param sigma: for autocanny
    :return:
    """
    kernel = np.ones((5, 5), np.uint8)
    imageslice = backgroundremoval(image, threshold)
    dilate = cv2.dilate(imageslice, kernel)
    erode = cv2.erode(dilate, kernel)
    closing = cv2.morphologyEx(imageslice, cv2.MORPH_CLOSE, kernel)
    blurred = cv2.GaussianBlur(closing, (5,5), 0)
    edges = auto_canny(np.uint8(blurred), sigma)
    if fill == True:
        edges = 255*sp.binary_fill_holes(edges).astype(int)
    return edges

def contour_coordinates(image, all = False, Rohan = False, im_show = False):

    """
    :param image: image to find all countours in
    :param all: if true, returns all, else returns largest one
    :param Rohan: for rohan's computer
    :return: list of coordinates of contours
    """

    if Rohan == True:
        contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        im, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rsx = []
    rex = []
    rsy = []
    rey = []
    if all == True:
        for c in range(len(contours)):
            cnts = contours[c]
            cv2.drawContours(image, [cnts], 0, (0,255,0), 3) # Draw the contours to the mask image
            x,y,w,h = cv2.boundingRect(cnts) #  get the bouding box information about the contour
            rsx.append(x)
            rex.append(x+w)
            rsy.append(y)
            rey.append(y+h)
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2) # Draw rectangle on the image to represent the bounding box
            if im_show == True:
                cv2.imshow("debug",image)
                cv2.waitKey()
        return rsx, rex, rsy, rey
    else:
        for c in range(len(contours)):
            lengths = [cv2.arcLength(c, True) for c in contours] # get the length of each contour
            max_index = np.argmax(lengths)
            cnts = contours[max_index]
            cv2.drawContours(image, [cnts], 0, (0,255,0), 3) # Draw the contours to the mask image
            x,y,w,h = cv2.boundingRect(cnts) #  get the bouding box information about the contour
            rsx.append(x)
            rex.append(x+w)
            rsy.append(y)
            rey.append(y+h)
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2) # Draw rectangle on the image to represent the bounding box
            if im_show == True:
                cv2.imshow("debug",image)
                cv2.waitKey()
        return rsx, rex, rsy, rey

def fluxcalculation(data,edges):
    """

    :param data: image file
    :param edges: edges files with 0/255
    :return: flux count
    """
    flux =  0
    for i in range(np.shape(edges)[0]):
        for j in range(np.shape(edges)[1]):
            if edges[i][j] == 255 :
                flux = flux + data[i][j]
    return flux



def fluxarray(image, Rohan = False, im_show = False):

    """
    :param image: image to find galaxy in
    :param Rohan: is rohan using it?
    :return: array of flux values
    """
    edges = np.uint8(sourcedetection(image, fill=True))
    rsx, rex, rsy, rey = contour_coordinates(edges, all=True, Rohan=Rohan, im_show=im_show)
    fluxvalues = []
    for i in range(len(rsx)):
        galaxy = image[rsy[i]:rey[i], rsx[i]:rex[i]]
        edges = np.uint8(sourcedetection(galaxy, fill=True))
        fluxvalues.append(fluxcalculation(galaxy, edges))
    return fluxvalues