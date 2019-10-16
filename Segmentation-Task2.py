#!/usr/local/bin/python3
#Creator: Stephen Alger
#Date 15-OCT-2019
#Threshold Segmentation Implementation

#Import Stuff...
import sys
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from matplotlib import image as image
#import easygui

img = cv2.imread('Googly.jpg',0)
ret,thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img,25,255,cv2.THRESH_BINARY)
ret,thresh3 = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
ret,thresh4 = cv2.threshold(img,75,255,cv2.THRESH_BINARY)
ret,thresh5 = cv2.threshold(img,100,255,cv2.THRESH_BINARY)

titles = ['Original Image','BINARY(127,255)','BINARY(25,255)','BINARY(50,255)','BINARY(75,255)','BINARY(100,255)']
images = [img, thresh, thresh2, thresh3, thresh4, thresh5]

for i in range(6):
    plt.subplot(2,3,i+1), plt.imshow(cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB))
    
    plt.title(titles[i])
plt.show()



