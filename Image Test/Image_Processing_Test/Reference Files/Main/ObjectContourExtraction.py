#!/usr/local/bin/python3
#Creator: Stephen Alger
#Version: 1.5 'Shark Attack - Extract The Shark!'
#Document: Assignment1.py
#Start-Date:  10-OCT-2019
#Object Image Extractor using Image Processing Techniques such as Hist Equalisation, Colour Space Manipulation, Thresholding and Contouring.

#Import Modules...
import sys, os, cv2, numpy as np, matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from matplotlib import pyplot as plt
import easygui

FILE_PATH = "./InputImages/"
FILE_OUT_NAME = "_EXTRACT"
FILE_OUT_PATH = "./OutputImages/"
SAMPLE_SCRIPT_RUN = "python3 ObjectContourExtraction.py 'Shark 2.PNG'"

#------Little bit of clean up
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

clear()

if sys.version_info[0]<3 :
    print("PYTHON 3 MINIMUM REQUIRED")
    exit()

#------Error In Arg Handling & File Input
ACCEPTED_FILETYPE = [".PNG",".png"]

#JPEG Removed & To Be readded - causing buggy behaviour
#ACCEPTED_FILETYPE = [".PNG",".png",".JPEG",".jpeg",".JPG",".jpg"]

ERROR_FILE_TYPE = True

#Check Number of Arguments
if len(sys.argv) == 2:
    for filetype in range(len(ACCEPTED_FILETYPE)) :
        if sys.argv[1].endswith(ACCEPTED_FILETYPE[filetype]):
            ERROR_FILE_TYPE = False
            
#            Save filetype for debug purposes
            ACCEPTED_FILETYPE = ACCEPTED_FILETYPE[filetype]
            break
            
    if ERROR_FILE_TYPE == True:
        print("File Type Selected is Not Supported (PNG only)")
#        print("File Type Selected is Not Supported (JPEG/PNG only)")
        exit()
else:
    print("Re-run This Script as follows: [ObjectExtraction.py] ['FileName.fileExtension']")
    print("Try: " + SAMPLE_SCRIPT_RUN)
    exit()


#FILE_NAME = "Shark 1.PNG"
FILE_NAME = sys.argv[1]
FILE_LOC = FILE_PATH + FILE_NAME
print("Loading File... [" + FILE_LOC + "]")


#-------GUI Input Method - Buggy & Commented Out
    
#version = str(tk.TkVersion)
#print("TK Version: [" + version + "]")
    
#Temperamental EASUGUI - to be added again - issues with deprecated tkinter
#FILE_LOC = str(easygui.fileopenbox(msg="Please Select An Image to Analyse", title="Image Selector", default=FILE_PATH, filetypes=[["*.png","*.PNG", "PNG files"], ["*.jpeg", "*.jpg","*.JPEG", "JPEG files"]]))



#-------User Prompt

print("Welcome to my Foreground and Background Analyser")
print("Please use the slider in the pop-up window to line up the White crosshairs with your object to make a selection")

winName = "Image Contour Analysis"

#-------Global Variables & Initialisation
src = cv2.imread(FILE_LOC)

dst = targetMask = brightness = src

dst = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
hue,saturation,brightness = cv2.split(dst)

#-------Default parameter settings as rough guide
useEqualise = 1
blurSize = 38
#threshold = int(33.0 * 255 / 100)
threshold = 98
blocksize = 11
offset = 11


#--------Function to let user analyse the thresholding process using sliders to add blur, equalisation and the threshold value to avoid artibrary hardcoding
def imageAnalyser(val):

    global useEqualise, blurSize, threshold, dst, src, blocksize,offset
    tempMatrix = brightness
    np.copyto(tempMatrix, brightness)

#    -----Stage 1: Add the Gassian Blur and Histogram Equalisation - contast stretching

    #Blocksize cant be even
    if (blocksize > 1 and (blocksize%2==0)):
        blocksize -= 1
    
    if (blurSize<8):
        blurSize = 8
        
    if (blurSize >= 3):
        blurSize = blurSize + (1 - blurSize % 2)
        tempMatrix    = cv2.GaussianBlur(tempMatrix, (blurSize, blurSize), 0)

    if (useEqualise):
        tempMatrix = cv2.equalizeHist(tempMatrix)

#    ------Apply threshold with slider settings - BINARY INVERSE Global Threshold
#    ret1, tempMatrix = cv2.threshold(tempMatrix,threshold,255, cv2.THRESH_BINARY_INV)
    
    tempMatrix = cv2.adaptiveThreshold(tempMatrix,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,255,4)
    
#    -------Design Using Adaptive Threshold Mean removed as it involves far too much hardcoding before useful in any portable way
#    tempMatrix = cv2.adaptiveThreshold(tempMatrix,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,11)
#    tempMatrix = cv2.bitwise_not(tempMatrix)

#    Display Analyser Window
    cv2.imshow(winName, mat = tempMatrix)

#    Return external contour matrices of objects found
    contours, hierarchy = cv2.findContours(tempMatrix,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#    Draw contours and locate the largest (its usually either background or the shark object)
    np.copyto(dst, src)
    maxDimension = 0
    largest = -1

#    --Green Contours - Aim to capture shark in this set of contours then use the mask created to subtract from the foreground
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
        dst    = cv2.polylines(dst, backgroundDebris, True, colour,2)
        cv2.drawContours(dst, contours, largest, colour, -1)

    
#    cv2.imshow(winName, dst)
    
#def selectCountour(contour):
    

#-----Callbacks on slider value update
def adjustEqualise(E):
    global useEqualise
    useEqualise = E
    boolE = bool(E)
    print("Threshold value is ["+ str(threshold) + "], Equalise value is ["+ str(E) + "], Gaussian Blur Size value is ["+ str(blurSize) + "]")
    imageAnalyser(0)
    
def adjustBlur(B):
    global blurSize
    blurSize = B
    boolE = bool(useEqualise)
    print("Threshold value is ["+ str(threshold) + "], Equalise value is ["+ str(boolE) + "], Gaussian Blur Size value is ["+ str(B) + "]")
    imageAnalyser(0)
    
def adjustThreshold(T):
    global threshold
    threshold = T
    boolE = bool(useEqualise)
    print("Threshold value is ["+ str(T) + "], Equalise value is ["+ str(boolE) + "], Gaussian Blur Size value is ["+ str(blurSize) + "]")
    imageAnalyser(0)
    
def adjustBlocksize(Blocksize):
    global blocksize
    blocksize = Blocksize
    imageAnalyser(0)
    
def adjustOffset(Offset):
    global offset
    offset = Offset
    imageAnalyser(0)

def cropMaskToROI():
    #Our dst image represents our contoured object
    #now we want to crop to this image and re contour
    global dst
    _,_,MASKROI = cv2.split(dst)

    
    cv2.imshow("MASKROI", MASKROI)
    cv2.waitKey(0)
    
    ## Calculates and returns point x, y, height and width of the shark in the mask
    (x,y,w,h) = cv2.boundingRect(MASKROI)
    print(x, y, w, h)
    
    #### Cropping the image to Shark co-ordinates ####
    x=x-25
    y=y-25
    w=x+w+25
    h=y+h+25

    if x<=0:
        x=25

    if y<=0:
        y=25

    #Final Image
    C = MASKROI[y:h, x:w]
    print(x, y, w, h)
    cv2.imshow("Cropped", C)
    cv2.waitKey(0)
    
def bitwiseSubtractor():
    global dst, src

#    Once the user picks a good threshold, EQ & blur the output shark is processed again
#    From Testing: Shark 1.png works best @ T=97, E= TRUE, B = 39
#    From Testing: Shark 2.png works best @ T=103, E= TRUE, B = 38
#    As I have a perfect mask of the shark output now we can do a simple threshold to grab the B&W mask we need...
    ret1, sharkMatrix = cv2.threshold(dst,250,255, cv2.THRESH_BINARY_INV)
    
    cv2.imshow("Your Selection...", sharkMatrix)
    cv2.waitKey(0)
    
    subMask = cv2.subtract(src, sharkMatrix)
    cv2.imshow("Submask Of Your Selection -OpenCV Subtraction", subMask)
    cv2.waitKey(0)
    
#    Invert background - Black to white
    gray = cv2.cvtColor(subMask, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 15, cv2.THRESH_BINARY)
    cv2.imshow("Post Background Invert", thresh)
    subMask[thresh == 0] = 255
    
#    Perform a little erosion for natural looking edges
    razor = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    erosionPhase = cv2.erode(subMask, razor, iterations = 1)
    cv2.imshow("Post Erosion Phase", erosionPhase)
    cv2.waitKey(0)
    
#    Destination Image extracted...
    dst = erosionPhase

#-------Trackbar setup with Callbacks to each above function
cv2.namedWindow(winname = winName, flags = cv2.WINDOW_NORMAL)
#cv.CreateTrackbar(trackbarName, windowName, value, count, onChange)
cv2.createTrackbar("Equalise", winName, useEqualise, 1, adjustEqualise)
cv2.createTrackbar("Blur Sigma", winName, blurSize, 100, adjustBlur)
#cv2.createTrackbar("Threshold", winName, threshold, 255, adjustThreshold)
#cv2.createTrackbar("Blocksize", winName, threshold, 255, adjustBlocksize)
#cv2.createTrackbar("Offset", winName, threshold, 255, adjustOffset)

#Call the functions!
imageAnalyser(0)
cv2.waitKey(delay = 0)


#cropMaskToROI()

#Cut out the Contoured Object...
bitwiseSubtractor()
#Viola! You've Got your shark - hopefully!


#Format Output Name file based on input filename
tmpName = sys.argv[1].split(ACCEPTED_FILETYPE)
tmpName[len(tmpName)-2]+= FILE_OUT_NAME
FILE_OUT_NAME = tmpName[len(tmpName)-2] + ACCEPTED_FILETYPE


#File location now refers to output file not input
FILE_LOC = FILE_OUT_PATH + FILE_OUT_NAME
print("Your Extraction Image Has Been Saved To File @ [" + FILE_LOC + "]")
cv2.imwrite(FILE_LOC, dst)

cv2.destroyAllWindows()

exit()


    
    



