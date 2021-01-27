#!/usr/local/bin/python3
#Creator: Stephen Alger C16377163
#Version: 1.0 'Assignment to Remove The Ball!'
#Document: Assignment2.py
#Start-Date:  08-NOV-2019
#Consult the README.md File attached for Algorithm & Process Description as to conform to the Rubric.

#------IMPORT MODULES
import sys, os, cv2, numpy as np, matplotlib
#matplotlib.use("TkAgg")
matplotlib.use("macOSX")
import tkinter as tk
from matplotlib import pyplot as plt

#------DEFINE CONSTANTS - PROGRAM SETUP
FILE_PATH = "./InputImages/"
FILE_OUT_NAME = "_MINUSBALL"
FILE_OUT_PATH = "./OutputImages/"
FILE_NAME_ARRAY = ["golf.jpg", "snooker.jpg", "spottheball.jpg"]
ACCEPTED_FILETYPE = [".PNG",".png",".JPEG",".jpeg",".JPG",".jpg"]



#CHOOSE INPUT FILE HERE!!!
#-------
FILE_NAME = FILE_NAME_ARRAY[2]
#-------


WINDOW_NAME = "Ball Removal"
print("OpenCV Version: {}".format(cv2.__version__))

#------COMMANDLINE CLEANUP
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
    if sys.version_info[0]<3:
        print("PYTHON 3 MINIMUM REQUIRED")
        exit()

#------FILE INPUT & ERROR HANDLING

ERROR_FILE_TYPE = True

for filetype in range(len(ACCEPTED_FILETYPE)) :
    if FILE_NAME.endswith(ACCEPTED_FILETYPE[filetype]):
        ERROR_FILE_TYPE = False
        ACCEPTED_FILETYPE = ACCEPTED_FILETYPE[filetype]
        break
        
if ERROR_FILE_TYPE == True:
    print("File Type Selected is Not Supported (PNG only)")
#        print("File Type Selected is Not Supported (JPEG/PNG only)")
    exit()
    
FILE_LOC = FILE_PATH + FILE_NAME
print("Loading File... [" + FILE_LOC + "]")

#-------Global Variables & Initialisation
src = cv2.imread(FILE_LOC)
dst = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
DIMENSIONS = src.shape
MAX_HEIGHT = DIMENSIONS[0]
MAX_WIDTH = DIMENSIONS[1]
NO_CHANNELS = DIMENSIONS[2]
IMAGES=[]
TITLES=[]
hue,saturation,brightness = cv2.split(dst)

#-------Default parameter settings - these are carefully chosen using Sliders
#Note: WHILE THIS IS HARDCODED FOR SUBMISSION THESE VALUES WERE GENERATED THROUGH PYTHON SLIDERS - REMOVED AT SUBMISSION TIME BASED ON FEEDBACK FROM ASSIGNMENT1
useEqualise = 1
blurSize = 17
threshold = 4
offset = 11

#-------Test Input Channels - CHOOSE MOST SUITABLE CHANNEL

def  testColourChannelInput(src):
    dst = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    hue,saturation,brightness = cv2.split(dst)
    lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
    L,A,B = cv2.split(lab)

    luv = cv2.cvtColor(src, cv2.COLOR_BGR2LUV)
    L,U,V = cv2.split(lab)

    xyz = cv2.cvtColor(src, cv2.COLOR_BGR2XYZ)
    X,Y,Z = cv2.split(lab)

    Images = [src, hue, saturation, brightness, L,A,B,L,U,V,X,Y,Z]
    Titles = ["Original Image", "H", "S", "V","L", "A", "B","L","U","V","X","Y","Z"]

    for i in range(13):
        plt.subplot(4, 4, i+1), plt.imshow(cv2.cvtColor(Images[i], cv2.COLOR_BGR2RGB))
        plt.title(Titles[i])
    plt.show()


#-------Main Functions

#imageAnalyser SETS THE STAGE, BASIC IMAGE ADJUSTMENTS & CALLS
#HIST_EQ, BINARY_THRESH - RETURNS BINARY MATRIX WITH FEW WHITE OBJECTS REMAINING, GIVING A ROUGH FOCUS POINT ON THE WHITE OBJECTS IN THE IMAGE
def imageAnalyser():
    global tempMatrix
    
    #FROM TESTING SATURATION CHANNEL OF HSV LOOKS MOST FITTING
    tempMatrix = saturation
    
    #HISTOGRAM EQUALISATION - HABITUAL, NOT REQUIRED
    if (useEqualise):
        tempMatrix = cv2.equalizeHist(tempMatrix)
    
    #USE OF GAUSSIAN BLUR FOR NOISE REDUCTION - INITIAL NOISE REDUCTION
    if blurSize != 0:
        tempMatrix    = applyBlur(tempMatrix)

    #APPLY UNIVERSAL THRESHOLD_BINARY_INVERSE
    tempMatrix = applyThreshold(tempMatrix, 1)

    return tempMatrix

#FUNCTION TO APPLY BLUR - NOTHING FANCY
def applyBlur(tempMatrix):
    tempMatrix    = cv2.GaussianBlur(tempMatrix, (blurSize, blurSize), 0)
    return tempMatrix

#FUNCTION TO APPLY BOTH BINARY REG & BINARY INVERSE - NOTHING FANCY
def applyThreshold(tempMatrix, flag):
    #Inverse Flag
    if flag == 1:
        #------Apply threshold with slider settings - BINARY INVERSE Global Threshold
        _, tempMatrix = cv2.threshold(tempMatrix,threshold,255, cv2.THRESH_BINARY_INV)
    else:
        #------Apply threshold with slider settings - BINARY REGULAR Global Threshold
        _, tempMatrix = cv2.threshold(tempMatrix,threshold,255, cv2.THRESH_BINARY)
    return tempMatrix

    
#Returns array of contours
def getContours(tempMatrix):
    contours, _ = cv2.findContours(tempMatrix,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return contours

#System is designed that the largest Contours generated from the Thresholded Mask (using my initial values) are the balls we want to obtain. So now we just need to locate the biggest contour!
#Returns sorted array of contours largest to smallest (discard most)
def sortContours(contours):
    global tempMatrix, dst
    np.copyto(dst, src)
    maxDimension = 0
    largest = -1
    for i in range(len(contours)):
        dimension = len(contours[i])
        if (dimension > maxDimension):
            maxDimension = dimension
            largest = i

    colour = (255, 255, 255)
    ballSelectionMask = np.zeros(shape = src.shape, dtype = "uint8")
    
    cv2.drawContours(ballSelectionMask, contours, largest, colour, cv2.FILLED)
#    r = cv2.selectROI(tempMatrix)
    return ballSelectionMask, largest
    

#ONCE WE HAVE LOCATED THE LARGEST CONTOUR, THE PROGRAM WILL MAKE AN ROI AROUND THE CONTOUR, NARROWING DOWN OUR BALL!
def createBoundingRect(ballSelectionMask, contours,largest):
    global src
    
    #CREATE RECT AROUND LARGEST CONTOUR - ADDING EXTRA SPACE AS WE STILL ONLY HAVE A PARTIAL REGION
    #THIS ALLOWS THE PROGRAM TO BUILD A BIGGER ROI CONTAINER WHICH WE CAN BE MORE PRECISE WITH
    x,y,w,h = cv2.boundingRect(contours[largest])
    x-= int(w*0.5)
    y-= int(h*0.5)
    w *= 2
    h *= 2
    
    if (x>=0 and y>=0):
        #DRAW RECT.
        cv2.rectangle(ballSelectionMask,(x,y),(x+w,y+h),(255,255,255), cv2.FILLED)
        return ballSelectionMask, x,y,w,h
    else:
        print("Negative X or Y Co-ordinates not prohibited, program closing")
        exit()

#FUNCTION TO FIND CIRCLES IN MASK & FILL APPROPRIATELY
def drawCircles(ballSelectionMask,w):
    #HoughCircles Implemented - USE OF FLEXIBLE MIN/MAX RADII TO CATER FOR DIFFERENT IMAGES AND IGNORE NONIMPORTANT CIRCLES- OFTEN MANY CIRCLES RETURNED OF NO SIGNIFICANCE WITHOUT STRONG PARAMETERS!
    circles = cv2.HoughCircles(ballSelectionMask,cv2.HOUGH_GRADIENT,2,200,param1=20,param2=10,minRadius=int(w*.25),maxRadius=int(w/2))
    
    #ERROR CHECK - IF NO CIRCLES RETURNED...
    if circles is None:
        print("No Hough Circles return")
        exit()

    #USING THE RETURNED CIRCLE - I HAVE BUILT A RECTANGLE AROUND ITS CORDINATES WHICH WORKS BETTER FOR INPAINT() THAN AN ELLIPTICAL OBJECT
    circles = np.uint16(np.around(circles))
    if len(circles) == 1:
        ballSelectionMask = np.zeros(shape = src.shape, dtype = "uint8")
        for    i in circles[0,:]:
            centre_x = i[0]
            centre_y = i[1]
            radius = i[2]
            startPointX =centre_x-int(radius*1.25)
            startPointY = centre_y-int(radius*1.1)
            endX = centre_x+int(radius*1.1)
            endY =centre_y+int(radius*2.25)
            circleROI = cv2.circle(ballSelectionMask,(centre_x,centre_y),radius,(255,255,255),cv2.FILLED)
            
            IMAGES.append(cv2.cvtColor(circleROI, cv2.COLOR_BGR2GRAY))
            TITLES.append("CircleROI")
            cv2.rectangle(ballSelectionMask,(startPointX,startPointY),(endX,endY),(255,255,255), cv2.FILLED)
            
    else:
        print("Too Many Hough Circles returned")
        exit()
    
#    RETURN OUR DESIRED MASK AND OUR BALL'S Points of interest
    return ballSelectionMask,startPointX,startPointY,endX,endY

#FUNCTION TO APPLY CV DIALTION ON BALL - CODE PREVIOUSLY USED, IS NOT USED AT SUBMISSION
def morphology_dialate(ballSelectionMask):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    ballSelectionMask = cv2.dilate(ballSelectionMask, kernel, iterations=3)
    cv2.imshow("DIALATE",ballSelectionMask)
    cv2.waitKey(delay = 0)
    return ballSelectionMask

#FUNCTION DESIGNED TO GET A GRASS SAMPLE
#ESSENTIALLY JUST A GREEN THRESHOLD ON HSV
#REMOVED - COULDN'T GET WORKING IN TIME
def getGrass(imageLessBall):
    image = cv2.cvtColor(imageLessBall, cv2.COLOR_BGR2HSV)

    applyBlur(image)
    
    lowColour = (50,127,127)
    highColour = (85, 255,255)
    
    grassMask = cv2.inRange(image, lowColour, highColour)
    
    return grassMask
    
#FUNCTION TO GET A LEGITIMATE SAMPLE ROI AROUND THE GAP
#THIS ATLEAST REDUCES THE NEED FOR INPAINT() UNLESS THERE IS NO OBTAINABLE SAMPLE
#REMOVED - COULDN'T GET WORKING IN TIME
def getSampleArea(grassMask):
    #BUILD an ROI around the ball, check if it overlaps with any background debris in grassMask, if not use this rect as a filler for the gap, otherwise use a different ROI
    startPointX,startPointY,endX,endY
    w = endX-startPointX
    
    rectMask = rect2Mask = 255*np.ones(shape = src.shape, dtype = "uint8")
    rectMask = cv2.rectangle(rect1Mask,(startPointX-w,startPointY),(endX-w,endY),(0,0,0), cv2.FILLED)
    
    intersects = ((rectMask & grassMask).area() > 0);
    
    return rectMask



#-------SIMPLE BITWISE FUNCTIONS - FEELS LIKE A SHORTCUT
def bitwiseAND(mask1, mask2):
    return (cv2.bitwise_and(mask1, mask2))
    
def bitwiseNOT(mask1, mask2):
    return (cv2.bitwise_not(mask1, mask2))

def bitwiseOR(mask1, mask2):
    return (cv2.bitwise_or(mask1, mask2))
    
def bitwiseXOR(mask1, mask2):
    return (cv2.bitwise_xor(mask1, mask2))

    
#-------CallBack Functions -> used in TRACKBAR DURING DEVELOPMENT, NOT CALLED AT SUBMISSION
def adjustThreshold(Threshold):
    global threshold
    threshold = Threshold
    print("Threshold: ",Threshold)
    imageAnalyser(0)
    
def adjustBlur(Blur):
    global blurSize
    blurSize = Blur
    if (blurSize<5):
        blurSize = 0
    if (blurSize >= 3):
        blurSize = blurSize + (1 - blurSize % 2)
    print("Blursize: ",blurSize)
    imageAnalyser(0)

#-------Trackbar setup with Callbacks to each above function
#REMOVED AT SUBMISSION - THESE WERE USED IN DEVELOPMENT TO AVOID HARDCODING VALUES AND BRUTE FORCE TO FIND BEST FITTING THRESHOLD VALUES
cv2.namedWindow(winname = WINDOW_NAME, flags = cv2.WINDOW_NORMAL)
#cv2.createTrackbar("Threshold", WINDOW_NAME, threshold, 255, adjustThreshold)
#cv2.createTrackbar("Blur Sigma", WINDOW_NAME, blurSize, 100, adjustBlur)

#-------Function Calls
clear()

#SIMPLE INPUT IMAGE ADJUSTMENTS AS EXPLAINED ABOVE
tempMatrix = imageAnalyser()
IMAGES.append(tempMatrix)
TITLES.append("ImageAdjustments")

#GET & SORT CONTOURS BY SIZE
contours = getContours(tempMatrix)
ballSelectionMask, largest = sortContours(contours)

#CREATE RECT AROUND BALL - NARROW DOWN THE SEARCH & CREATE MASK
ballSelectionMask, x,y,w,h = createBoundingRect(ballSelectionMask, contours, largest)
ballSelectionMask = bitwiseAND(src, ballSelectionMask)
ballSelectionMask=cv2.cvtColor(ballSelectionMask, cv2.COLOR_BGR2GRAY)

IMAGES.append(ballSelectionMask)
TITLES.append("DrawContours-RoughROI")

#RE-USE OF BLUR & THRESHOLDING TO COMPLETE THE MASK WHICH PARTIALLY CONTAINS OUR BALL
blurSize = 9
ballSelectionMask = applyBlur(ballSelectionMask)
threshold = 130
ballSelectionMask = applyThreshold(ballSelectionMask,0)


#NOW WE CREATE A DEFINED ROI MASK - RECT ENCOMPASSING THE BALL
ballSelectionMask,startPointX,startPointY,endX,endY = drawCircles(ballSelectionMask,w)
ballSelectionMask=cv2.cvtColor(ballSelectionMask, cv2.COLOR_BGR2GRAY)

IMAGES.append(ballSelectionMask)
TITLES.append("RectROI")



#USE INPAINT TO CONTENT AWARE FILL - V. BASIC ALGORITHM, RESULTS ARE POOR
#imageLessBall = cv2.inpaint(src,ballSelectionMask,0.1,cv2.INPAINT_NS)
imageLessBall = cv2.inpaint(src,ballSelectionMask,20,cv2.INPAINT_TELEA)

#USER Prompt
print("*********************************************************************\n");
print("||            Press ANY key to View The Phase Breakdown            ||\n");
print("*********************************************************************\n");
print("\nSelect the Python Window & Press Any Key\n");

cv2.imshow(WINDOW_NAME, imageLessBall)
cv2.waitKey(delay = 0)

IMAGES.append(cv2.cvtColor(imageLessBall, cv2.COLOR_BGR2GRAY))
TITLES.append("InpaintPerformed")


#USER OUTPUT - SHOW BREAKDOWN STAGES - CAN BE GLITCHY DEPENDING ON MATPLOTLIB version & system - comment out if causing crash
for i in range(len(IMAGES)):
    plt.subplot(2, 3, i+1), plt.imshow(IMAGES[i], cmap='gray')
    plt.title(TITLES[i])
plt.show()



#REMOVED AT SUBMISSION
#blurSize = 201
#grassMask = getGrass(imageLessBall)
#debris_Contours = getContours(grassMask)
#rectMask = getSampleArea(grassMask)

#Format Output Name file based on input filename
tmpName = FILE_NAME.split(ACCEPTED_FILETYPE)
tmpName[len(tmpName)-2]+= FILE_OUT_NAME
FILE_OUT_NAME = tmpName[len(tmpName)-2] + ACCEPTED_FILETYPE

FILE_LOC = FILE_OUT_PATH + FILE_OUT_NAME
print("Your Extraction Image Has Been Saved To File @ [" + FILE_LOC + "]")
cv2.imwrite(FILE_LOC, imageLessBall)

cv2.destroyAllWindows()
exit()
