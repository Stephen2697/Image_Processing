import numpy as np
import cv2
from matplotlib import pyplot as plt

image_Colour = cv2.imread('Shark 1.png')

mask = np.zeros(image_Colour.shape[:2], np.uint8)
   
backgroundModel = np.zeros((1, 65), np.float64)
foregroundModel = np.zeros((1, 65), np.float64)
   
rectangle = (200, 200, 600, 250)
   
# apply the grabcut algorithm with appropriate
# values as parameters, number of iterations = 3
# cv2.GC_INIT_WITH_RECT is used because
# of the rectangle mode is used
cv2.grabCut(image_Colour, mask, rectangle,
            backgroundModel, foregroundModel,
            3, cv2.GC_INIT_WITH_RECT)
   
# In the new mask image, pixels will
# be marked with four flags
# four flags denote the background / foreground
# mask is changed, all the 0 and 2 pixels
# are converted to the background
# mask is changed, all the 1 and 3 pixels
# are now the part of the foreground
# the return type is also mentioned,
# this gives us the final mask
mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
   
# The final mask is multiplied with
# the input image to give the segmented image.
image_Colour = image_Colour * mask2[:, :, np.newaxis]
   
# output segmented image with colorbar
plt.imshow(image_Colour)
plt.colorbar()
plt.show()
