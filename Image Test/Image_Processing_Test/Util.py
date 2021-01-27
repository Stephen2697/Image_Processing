#!/usr/local/bin/python3
#Creator: Stephen Alger
#Creator Deatils: C16377163 DT228/4
#Version: 1.0 'Doc Name'
#Document: Test.py
#Start-Date:  09-DEC-2019
#File Function: Utility Functions Go Here, To Remove standardised environment functions from the core code in Main.py

import os, cv2, matplotlib,sys
matplotlib.use("macOSX")
from matplotlib import pyplot as plt


#------DEFINE CONSTANTS - PROGRAM SETUP
FILE_PATH = "./InputImages/"
ACCEPTED_FILETYPE = [".PNG",".png",".JPEG",".jpeg",".JPG",".jpg"]

#------For A Tidy User Experience - Function to Clear Command Line
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

#------Check For Correct Version of Python - Designed, Built & Tested for Python 3
def checkPythonVerions():
    if sys.version_info[0]<3 :
        print("PYTHON 3 MINIMUM REQUIRED")
        exit()

#------Load Input with Error Handling - Flag Errors
def loadFile(FILE_NAME):
    global ACCEPTED_FILETYPE
    ERROR_FILE_TYPE = True

    for filetype in range(len(ACCEPTED_FILETYPE)) :
        if FILE_NAME.endswith(ACCEPTED_FILETYPE[filetype]):
            ERROR_FILE_TYPE = False
            ACCEPTED_FILETYPE = ACCEPTED_FILETYPE[filetype]
            break
            
    if ERROR_FILE_TYPE == True:
        print("File Type Selected is Not Supported (JPEG/PNG only)")
        exit()
        
    FILE_LOC = FILE_PATH + FILE_NAME
    print("\nLoading File... [" + FILE_LOC + "]\n")
    inputImage = cv2.imread(FILE_LOC)
    
    if inputImage is None:
        print("Image Input Failed")
        exit()
    return inputImage
#    end def

#-------Return Image Dimensions
def getImageDimensions(inputImage):
    DIMENSIONS = inputImage.shape
    HEIGHT = DIMENSIONS[0]
    WIDTH = DIMENSIONS[1]
    return HEIGHT, WIDTH
#    end def

#-------Test Channels
def testColourChannelInput(src):
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

