#-----------
import cv2, sys, numpy as np


img = cv2.imread('Shark 1.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([30,150,50])
upper_red = np.array([255,255,180])

mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(img,img, mask= mask)

#cv2.imshow('Original',img)
#key = cv2.waitKey(0)

edges = cv2.Canny(img,100,200)
cv2.imshow('Edges',edges)
key = cv2.waitKey(0)
