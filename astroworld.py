import numpy as np
from astropy.io import fits
import cv2
import matplotlib.pyplot as plt



hdulist = fits.open("A1_mosaic.fits")

image = hdulist[0].data
hist = np.sum(image, axis = 0)
print(np.argmax(hist))
plt.plot(hist)
plt.show()
#image_info = hdulist.info()




#print(image)


#img = cv2.imread("galaxies.jpeg")

#print(img)
kernel = (1/25)*np.array([[0,0,0,0,0],[0,0,0,0,0],[5,5,5,5,5],[0,0,0,0,0],[0,0,0,0,0]])
dst = cv2.GaussianBlur(img, (5,5),0)
dst = cv2.filter2D(image,-1,kernel)



edges = cv2.Canny(dst,0,5)

plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()
