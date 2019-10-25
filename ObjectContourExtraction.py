#!/usr/local/bin/python3
#Creator: Stephen Alger C16377163
#Assignment: 1 'Shark Attack'
#Document: Assignment1.py
#Start-Date:  10-OCT-2019
#Shark Image Extractor using Analysis

#Import Modules...
import sys, os, cv2, numpy as np, matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import *

#-------Get Input File from user
#Incompatible with my system, easygui acting up too, manaul input unfortunately
#root = tk.Tk()
#root.withdraw()
#file_path = filedialog.askopenfilename()

file_path = "Shark 1.png"
print(file_path)

#------Error Handling

if not (file_path.endswith('.png') or file_path .endswith('.PNG ')):
	print("Analyser Error - File must be PNG or JPEG")
	exit()
	
#-------User Prompt

print("Welcome to my Foreground and Background Analyser")
print("Please use the slider to line up the White crosshairs with your object to make a selection")

winName = "Shark Analysis"

#-------Global Variables & Initialisation
src = dst = targetMask = brightness = cv2.imread(file_path)
dst = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
hue,saturation,brightness = cv2.split(dst)

#-------Default parameter settings as rough guide
useEqualise = 1
blursSize = 21
threshold = int(33.0 * 255 / 100)

#--------Function to let user analyse the thresholding process using sliders to add blur, equalisation and the threshold value to avoid artibrary hardcoding
def imageAnalyser(val):

	global useEqualise, blursSize, threshold, dst, src
	tempMatrix = brightness
	np.copyto(tempMatrix, brightness)

#	-----Stage 1: Add the Gassian Blur and Histogram Equalisation - contast stretching
	if (blursSize >= 3):
		blursSize += (1 - blursSize % 2)
		tempMatrix	= cv2.GaussianBlur(tempMatrix, (blursSize, blursSize), 0)
	if (useEqualise):
		tempMatrix = cv2.equalizeHist(tempMatrix)

#    ------Apply threshold with slider settings - BINARY INVERSE Global Threshold
	ret1, tempMatrix = cv2.threshold(tempMatrix,threshold,255, cv2.THRESH_BINARY_INV)
	
	
#	-------Design Using Adaptive Threshold Mean removed as it involves far too much hardcoding before useful in any portable way
#	tempMatrix = cv2.adaptiveThreshold(tempMatrix,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,11)
#	tempMatrix = cv2.bitwise_not(tempMatrix)

#	Display Analyser Window
	cv2.imshow(winName, mat = tempMatrix)

#	Return external contour matrices of objects found
	contours, hierarchy = cv2.findContours(tempMatrix,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#	Draw contours and locate the largest (its usually either background or the shark object)
	np.copyto(dst, src)
	maxDimension = 0
	largest = -1

#	--Green Contours - Aim to capture shark in this set of contours then use the mask created to subtract from the foreground
	for i in range(len(contours)):
		colour = (0, 255, 0)
		cv2.drawContours(dst, contours, largest, colour, 1)
		cv2.fillPoly(dst, contours, color=(255,255,255))
		dimension = len(contours[i])
		if (dimension > maxDimension):
			maxDimension = dimension
			largest = i

#------Red Contours

	#Red contours should be used to identify background features separate from foreground
	targetMask = np.zeros(len(src), dtype=np.uint8)
	colour = (0, 0, 0)
	if (largest >= 0):
		backgroundDebris = contours[largest]
		dst	= cv2.polylines(dst, backgroundDebris, True, colour,2)
		cv2.drawContours(dst, contours, largest, colour, -1)

	
	cv2.imshow(winName, dst)
	

#-----Callbacks on slider value update
def adjustEqualise(E):
	global useEqualise
	useEqualise = E
	boolE = bool(E)
	print("Threshold value is ["+ str(threshold) + "], Equalise value is ["+ str(E) + "], Gaussian Blur Size value is ["+ str(blursSize) + "]")
	imageAnalyser(0)
	
def adjustBlur(B):
	global blursSize
	blursSize = B
	boolE = bool(useEqualise)
	print("Threshold value is ["+ str(threshold) + "], Equalise value is ["+ str(boolE) + "], Gaussian Blur Size value is ["+ str(B) + "]")
	imageAnalyser(0)
	
def adjustThreshold(T):
	global threshold
	threshold = T
	boolE = bool(useEqualise)
	print("Threshold value is ["+ str(T) + "], Equalise value is ["+ str(boolE) + "], Gaussian Blur Size value is ["+ str(blursSize) + "]")
	imageAnalyser(0)


def bitwiseSubtractor():
	global dst, src

#	Once the user picks a good threshold, EQ & blur the output shark is processed again
#	From Testing: Shark 1.png works best @ T=97, E= TRUE, B = 39
#	From Testing: Shark 2.png works best @ T=103, E= TRUE, B = 38
#	As I have a perfect mask of the shark output now we can do a simple threshold to grab the B&W mask we need...
	ret1, sharkMatrix = cv2.threshold(dst,250,255, cv2.THRESH_BINARY_INV)
	
	cv2.imshow("Your Selection...", sharkMatrix)
	cv2.waitKey(0)
	
	subMask = cv2.subtract(src, sharkMatrix)
	cv2.imshow("Submask Of Your Selection -OpenCV Subtraction", subMask)
	cv2.waitKey(0)
	
#	Invert background - Black to white
	gray = cv2.cvtColor(subMask, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 0, 15, cv2.THRESH_BINARY)
	cv2.imshow("Post Background Invert", thresh)
	subMask[thresh == 0] = 255
	
#	Perform a little erosion for natural looking edges
	razor = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
	erosionPhase = cv2.erode(subMask, razor, iterations = 1)
	cv2.imshow("Post Erosion Phase", erosionPhase)
	cv2.waitKey(0)
	
#	Viola! You've Got your shark - hopefully!


#-------Analyser Output & Trackbar setup with Callbacks to each above function
cv2.namedWindow(winname = winName, flags = cv2.WINDOW_NORMAL)
#cv.CreateTrackbar(trackbarName, windowName, value, count, onChange)
cv2.createTrackbar("Equalise", winName, useEqualise, 1, adjustEqualise)
cv2.createTrackbar("Blur Sigma", winName, blursSize, 100, adjustBlur)
cv2.createTrackbar("Threshold", winName, threshold, 255, adjustThreshold)

#Call the functions!
imageAnalyser(0)
cv2.waitKey(delay = 0)

bitwiseSubtractor()

exit()


	
	





