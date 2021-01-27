#!/usr/local/bin/python3
#Creator: Stephen Alger
#Creator Deatils: C16377163 DT228/4
#Version: 1.0 'Ruler Measurer'
#Document: Main.py
#Start-Date:  09-DEC-2019
#File Function: Measure The Ruler!
#Design Implemented:
'''
- Extract Our Desired Mask with Threshold on saturation in HSV
- Get Contours of resulting mask
- Get corner points of Rect
- Calculate the average lengths of the two long ruler sides
- Draw border and Put text to screen
- Output feedback to user
'''


#Import Modules...
import sys, cv2, numpy as np, matplotlib
matplotlib.use("macOSX")
import tkinter as tk
from matplotlib import pyplot as plt
from imutils import perspective
from imutils import contours
import imutils
import math

# local imports
from Util import clear, loadFile, checkPythonVerions

FILE_NAME_ARRAY = ["Ruler.PNG"]
FILE_NAME = FILE_NAME_ARRAY[0]

BLURSIZE = 17
RULER_CM_LENGTH = 101

#FUNCTION TO APPLY BLUR - NOTHING FANCY
def applyBlur(tempMatrix):
    tempMatrix = cv2.GaussianBlur(tempMatrix, (BLURSIZE, BLURSIZE), 0)
    return tempMatrix


#FUNCTION DESIGNED TO RETURN MASK OF RULER
#ESSENTIALLY JUST A YELLOW THRESHOLD ON HSV Saturation Channel
def isolateSaturationChannel(inputImage):
    HSV_image = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)
    _,saturation,_ = cv2.split(HSV_image)

    applyBlur(saturation)
    ret,thresholdMask = cv2.threshold(saturation,127,255,cv2.THRESH_BINARY)
    return thresholdMask
    
#Returns array of contours
def getContours(mask):
    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return contours

#System is designed that the largest Contours generated from the Thresholded Mask
#Returns sorted array of contours largest to smallest (discard most)
def sortContours(inputImage, contours):
    maxDimension = 0
    largest = -1
    for i in range(len(contours)):
        dimension = len(contours[i])
        if (dimension > maxDimension):
            maxDimension = dimension
            largest = i
    
    colour = (0, 0, 255)
    cv2.drawContours(inputImage, contours, largest, colour, 2)
 
    return inputImage, largest

#Dissect The Largest Contour to Get Corner Points & Calculate the Avg of the two lengths
def getCornerPoints(inputImage, largest, contours):
    #Calculate bounding box of the contour
    rect = cv2.minAreaRect(contours[largest])
    rect = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
    rect = np.array(rect, dtype="int")

    #Order the end points - so we know which sides are which
    rect = perspective.order_points(rect)
    
    #Get distnace of longest sides
    dist1 = calculateDistance(rect[0,0], rect[0,1],rect[1,0], rect[1,1])
    dist2 = calculateDistance(rect[3,0], rect[3,1],rect[2,0], rect[2,1])
    
    #Get avg side length
    avgDist = int((dist1+dist2)/2)
    return avgDist

#Get the Average Length Distance of the longest angles
def calculateDistance(x1,y1,x2,y2):
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
     return dist

def calculatePixelsPerCM(avgDist):
    pixelsPerCM = avgDist/ RULER_CM_LENGTH
    return pixelsPerCM
    
    

#ONCE WE HAVE LOCATED THE LARGEST CONTOUR, THE PROGRAM WILL MAKE AN ROI AROUND THE CONTOUR, NARROWING DOWN OUR BALL!
def createBoundingRect(inputImage, contours, largest):
    
    #CREATE RECT AROUND LARGEST CONTOUR - ADDING EXTRA SPACE AS WE STILL ONLY HAVE A PARTIAL REGION
    #THIS ALLOWS THE PROGRAM TO BUILD A BIGGER ROI CONTAINER WHICH WE CAN BE MORE PRECISE WITH
    x,y,w,h = cv2.boundingRect(contours[largest])
    
    if (x>=0 and y>=0):
        #DRAW RECT.
#        cv2.rectangle(inputImage,(x,y),(x+w,y+h),(0,0,255), 1)
        return inputImage, x,y,w,h
    else:
        print("Negative X or Y Co-ordinates prohibited, program closing")
        exit()

#Main Function - All the function calls here!
def main():

    #Clear Command line
    clear()
    
    #Check User is running right OpenCV version
    checkPythonVerions()
    
    #Open Image
    inputImage = loadFile(FILE_NAME)
    
    #Get Dimensions
    DIMENSIONS = inputImage.shape
    MAX_HEIGHT = DIMENSIONS[0]
    MAX_WIDTH = DIMENSIONS[1]

    #Create Mask on Saturation Channel
    mask = isolateSaturationChannel(inputImage)
    
    cv2.imshow("Our Ruler Mask - Post Threshold", mask)
    cv2.waitKey(0)
    
    contours = getContours(mask)
    inputImage, largest = sortContours(inputImage, contours)
    
    #CREATE RECT AROUND BALL - NARROW DOWN THE SEARCH & CREATE MASK
    boundingRectImage, x,y,w,h = createBoundingRect(inputImage, contours, largest)
        
    cv2.imshow("Our Bounding Rectangles", inputImage)
    cv2.waitKey(0)
    
    avgDist = getCornerPoints(inputImage, largest, contours)
    print("\nThis Ruler is",avgDist,"pixels in length!")
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(inputImage,str(avgDist),(int(MAX_HEIGHT/2), int(MAX_WIDTH/2)), font, .5,(255,0,0),2,cv2.LINE_AA)
    cv2.imshow("Our Measurements", inputImage)
    cv2.waitKey(0)
    
    pixelsPerCM = int(calculatePixelsPerCM(avgDist))
    
    print("\nThere are ~",pixelsPerCM, "pixels per Centimeter on this Ruler")
    
main()



