import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from tqdm import tqdm
import cv2 as cv2
import scipy.ndimage.morphology as sp
import scipy.stats as sps

def masking(data, splice_y, splice_x, ystart, yend, xstart, xend, a_lot = False):
    """
    :param data: image whose edges need to be masked
    :param xstart: starting value of edges (x axis)
    :param xend:  last value of edges (x axis)
    :param ystart: starting values of edges (y axis)
    :param yend: last value of edges (x axis)
    :return: masked image
    """
    array = np.copy(data)
    if a_lot == True:
        for x in range(len(xstart)):
            for i in range(splice_y + ystart[x], splice_y + yend[x]):
                for j in range(splice_x + xstart[x], splice_x + xend[x]):
                    array[i][j] = 3421
        return array
    else:
        for i in range(splice_y + ystart, splice_y + yend):
            for j in range(splice_x + xstart, splice_x + xend):
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
    kernel = np.ones((5,5), np.uint8)
    imageslice = backgroundremoval(image, threshold)
    dilate = cv2.dilate(imageslice, kernel)
    erode = cv2.erode(dilate, kernel)
    closing = cv2.morphologyEx(erode, cv2.MORPH_CLOSE, kernel)
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
    min = np.min(data)
    for i in range(np.shape(edges)[0]):
        for j in range(np.shape(edges)[1]):
            if edges[i][j] == 255 and min < 3421:
                flux = flux + data[i][j] - 3421
            else:
                flux = flux + data[i][j] - min
    return flux


def fluxcalculationnormalnoise(data,edges):
    """
    :param data: image file
    :param edges: edges files with 0/255
    :return: flux count
    """
    flux =  0
    min = np.min(data)
    for i in range(np.shape(edges)[0]):
        for j in range(np.shape(edges)[1]):
            if edges[i][j] == 255:
                flux = flux + data[i][j] - np.random.normal(3421,16)
    return np.int(flux)

def fluxcalculation2(data,edges):
    """
    :param data: image file
    :param edges: edges files with 0/255
    :return: flux count
    """
    star =  []
    background = []
    for i in range(np.shape(edges)[0]):
        for j in range(np.shape(edges)[1]):
            if edges[i][j] == 255:
                star.append(data[i][j])
            else:
                background.append(data[i][j])
    backgroundmean = np.average(background)
    flux = np.sum([i- backgroundmean for i in star])
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
        fluxvalues.append(fluxcalculationnormalnoise(galaxy, edges))
    return fluxvalues

def magnitudes(fluxarray,magzpt):
    """
    calculate instrumental magnitudes and convert to calibrated magnitude
    """
    mag_i =[]
    mags = []
    for i in range(len(fluxarray)):
        mag_i.append(-2.5* np.log10(fluxarray[i]))
        for j in range(len(mag_i)):
            mags.append(mag_i[j]+magzpt)
    return mags

def producecatalogue(image,ystart, yend, xstart, xend, splice_y = 0, splice_x = 0, catalogue = []):
    """
    :param image: entire image
    :param catalogue: list of 4d azarrays containing information about the bounding box around detected object
    :param splice_y: y coordinate if detected object comes from image splice
    :param splice_x: x coordinate if detected object comes from image splice
    :param xstart, xend: width of bounding boxes
    :param ystart, yend: length of bounding boxes
    """
    data = np.copy(iamge)
    for i in range(len(xstart)):
        catalogue.append(splice_y + ystart[i], splice_y + yend[i], splice_x + xstart[i], splice_x + xend[i])
        masked = masking(data, splice_y, splice_x, ystart[i], yend[i], xstart[i], xend[i])
    return masked, catalogue

"""
def classify(data):
    if data

"""
