import cv2, sys, numpy as np

def fixedThresh():
    global img, blur, thresh
    (t, mask) = cv2.threshold(src = blur, thresh = thresh, maxval = 255, type = cv2.THRESH_BINARY)

    sel = cv2.bitwise_and(src1 = img, src2 = mask)
    cv2.imshow(winname = "image", mat = sel)
   

def adjustThresh(v):
    global thresh
    thresh = v
    fixedThresh()
    

# read image as grayscale, and blur it

img = cv2.imread('Shark 1.png', flags = cv2.IMREAD_GRAYSCALE)
blur = cv2.GaussianBlur(src = img, ksize = (5, 5), sigmaX = 0)

# create the display window and the trackbar
cv2.namedWindow(winname = "image", flags = cv2.WINDOW_NORMAL)
thresh = 128
cv2.createTrackbar("thresh", "image", thresh, 255, adjustThresh)

# perform first thresholding
fixedThresh()
cv2.waitKey(delay = 0)



