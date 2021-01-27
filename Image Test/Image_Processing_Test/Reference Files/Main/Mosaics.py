#!/usr/local/bin/python3
#Creators: Stephen Alger C16377163/ Chris Clarke C16398141
#Version: 1.0 'Mosaics'
#Implemented Solution (Make Uniform Mosaic & Polygonal Mosaics)
#Document: README.txt - Documents the Program Info

#------IMPORT MODULES
import cv2, numpy as np, matplotlib
#matplotlib.use("macOSX")
from matplotlib import pyplot as plt

#------DEFINE CONSTANTS - PROGRAM SETUP
FILE_PATH = "./InputImages/"
FILE_OUT_PATH = "./OutputImages/"
FILE_OUT_NAME = ["_UniformMosaic","_BorderedMosaic","_BorderedTessellatedMosaic", "_TessellatedMosaic"]
FILE_NAME_ARRAY = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg"]
ACCEPTED_FILETYPE = [".PNG",".png",".JPEG",".jpeg",".JPG",".jpg"]
WINDOW_NAME = "THRESHOLD!"
threshold = 127 #initial

#CHOOSE INPUT FILE HERE!!!
#-------
FILE_NAME = FILE_NAME_ARRAY[1]

#-------

#-------UNIFORM TILE FUNCTIONS
def avgColourFill(inputImage):
    tempImage = inputImage.copy()
    HEIGHT, WIDTH = getImageDimensions(tempImage)
    TILE_SIZE, _ = getAdaptiveMeasurements(WIDTH)
    print("Width: [", WIDTH,"], Height: [", HEIGHT,"]")
    
#   Traverse X&Y -> Overwriting Tile Data with the Tiles' Average Colours
    i = j = 0
    while i<HEIGHT:
        while j<WIDTH:
#            get rect vertices
            x1, x2, y1, y2 = j, j+TILE_SIZE, i, i+TILE_SIZE
#            Get Average pixel data values within [x1,y1 - x2,y2]
            avgColour = tempImage[y1:y2, x1:x2].mean(0).mean(0)
#            Overwrite pixel colour data with pixel averages
            tempImage[y1:y2, x1:x2] = avgColour
            j += TILE_SIZE
        j=0
        i += TILE_SIZE
    return tempImage
#    end def

#Add Tile Bordering - Same story just draw the Colour Matched Borders
def addTileBorders(inputImage):
    tempImage = inputImage.copy()
    HEIGHT, WIDTH = getImageDimensions(tempImage)
    TILE_SIZE, BORDER_SIZE = getAdaptiveMeasurements(WIDTH)
#   Get Average Image Colour - Use for Borders
    borderColor = tempImage[0:HEIGHT, 0:WIDTH].mean(0).mean(0)
    i = j = 0
    while i<HEIGHT:
        while j<WIDTH:
#           Get rect vertices
            x1, x2, y1, y2 = j, j+TILE_SIZE, i, i+TILE_SIZE
#           Draw our tile borders
            cv2.rectangle(tempImage, (x1,y1), (x2,y2), borderColor, BORDER_SIZE)
            j += TILE_SIZE
        j=0
        i += TILE_SIZE
    return tempImage
#    end def

#Return Scaled Measurements
def getAdaptiveMeasurements(WIDTH):
    SCALE_FACTOR = int(WIDTH/600)
    TILE_SIZE = int(SCALE_FACTOR*7.5)
    BORDER_SIZE = int(SCALE_FACTOR*0.75)
    return TILE_SIZE, BORDER_SIZE
#    end def
    
#Return UNIFORM AVERAGED TILES & UNIFORM AVERAGED TILES WITH BORDERING
def makeUniformMosaic(inputImage):
    #Apply Colour Averaging
    uniformMosaic = avgColourFill(inputImage)
    #Apply Borders
    uniformBorderMosaic = addTileBorders(uniformMosaic)
    return uniformMosaic, uniformBorderMosaic
#    end def
    
#-------TESSELLATION TILE FUNCTIONS
    
#Return Contours of the Inputted Tresholded Image
def getContours(inputImage):
    imgray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, threshold, 255, 0) #CHANGE
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
#    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours
#    end def
    
#Format Contours of the Inputted Tresholded Image & Insert to SubDiv
def formatContourToSubDiv(contours, inputImage):
    #Set environment variables
    HEIGHT, WIDTH = getImageDimensions(inputImage)
    canvas = (0, 0, WIDTH, HEIGHT)
        
    # Instantiate Subdiv2D
    Subdiv = cv2.Subdiv2D(canvas)
    
    # Format contour points into Subdiv
    for contourPoint in contours :
        Subdiv.insert(contourPoint)
    
    return Subdiv
#    end def


def increaseContrast(inputImage):
    increasedContrastImage = inputImage.copy()
    
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    CLAHE = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))

    lab = cv2.cvtColor(increasedContrastImage, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels

    l2 = CLAHE.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2,a,b))  # merge channels
    
    increasedContrastImage = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    return increasedContrastImage

#Perform Tessellation Via OpenCv subdiv Voronoi Implementaion
def addTessellation(inputImage, Subdiv, Flag) :
    tessellatedMosaic = inputImage.copy()
    
    tessellatedMosaic = increaseContrast(tessellatedMosaic)
    
    #Returns a list of all the Voronoi facets (Polygonal Sides) and Centers
    (facetList, centers) = Subdiv.getVoronoiFacetList([])

    #Traverse each point in each the Voronoi Sides
    for i in range(0,len(facetList)) :
        #Use the returned Polygonal Centres co-ords to set Colour
        colour = np.uint8(inputImage[ np.int(centers[i][1]), np.int(centers[i][0]) ])
        colour = tuple(map(int, colour))
        #Array to store all the points on this side
        arrayOfFacetPoints = []
        #Unwrap Each XY Co-ordinate and append to our list
        for pointXY in facetList[i] :
            arrayOfFacetPoints.append(pointXY)
            #type cast to np.array
            tempFacetPntArray = np.array(arrayOfFacetPoints, np.int)
            #Fill the Polygon
            cv2.fillConvexPoly(tessellatedMosaic, tempFacetPntArray, colour, cv2.LINE_AA, 0)
            if Flag:  #Draw the Lines!
                cv2.polylines(tessellatedMosaic, [tempFacetPntArray], True, (255, 255, 255), 1, cv2.LINE_AA, 0)
    return tessellatedMosaic
#    end def

#Pull It All together and feed the addTessellation function
def makePolygonalMosaic(inputImage):
    #Get Contours as a set of basis points for Voronoi
    contours = getContours(inputImage)
    
    #Format Subdiv
    Subdiv  = formatContourToSubDiv(contours, inputImage)
    
    #Allocate space for Tessellated Voronoi Implementation
    tessellatedMosaic = np.zeros(inputImage.shape, dtype = inputImage.dtype)
    
    #Let it Rip!
    tessellatedMosaic = addTessellation(inputImage, Subdiv, 0)
    tessellatedMosaicWithPolyLines = addTessellation(inputImage, Subdiv, 1)
    return tessellatedMosaic, tessellatedMosaicWithPolyLines

#----GENERAL FUNCTION CALLS

#Load Input with Error Handling - Flag Errors
def loadFile():
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
    print("Loading File... [" + FILE_LOC + "]")
    inputImage = cv2.imread(FILE_LOC)
    
    if inputImage is None:
        print("Image Input Failed")
        exit()
    
    return inputImage
#    end def
    
#Return Image Dimensions
def getImageDimensions(inputImage):
    DIMENSIONS = inputImage.shape
    HEIGHT = DIMENSIONS[0]
    WIDTH = DIMENSIONS[1]
    return HEIGHT, WIDTH
#    end def

#Output to File
def outputFile(outputImage, processType):
    
    #File Output - Handle Adaptive File Naming
    tmpName = FILE_NAME.split(ACCEPTED_FILETYPE)
    processDescription = " "
    if processType == 0: #AVG-NO-BORDER-UNIFORM MOSAIC
        tmpName[len(tmpName)-2] += FILE_OUT_NAME[processType]
        processDescription = "Uniform Mosaic"
    elif processType == 1: #AVG-WITH-BORDER-UNIFORM MOSAIC
        tmpName[len(tmpName)-2] += FILE_OUT_NAME[processType]
        processDescription = "Bordered Uniform Mosaic"
    elif processType == 2:
        tmpName[len(tmpName)-2] += FILE_OUT_NAME[processType]
        processDescription = "Voronoi Polygonal Mosaic"
    else:
        tmpName[len(tmpName)-2] += FILE_OUT_NAME[processType]
        processDescription = "Voronoi Mosaic Without Poly Lines"
        
    #Build File Output Name
    tempName = tmpName[len(tmpName)-2] + ACCEPTED_FILETYPE
    FILE_LOC = FILE_OUT_PATH + tempName
    print("Your "+ processDescription +" Image Has Been Saved To File @ [" + FILE_LOC + "]")
    cv2.imwrite(FILE_LOC, outputImage)
#    end def



#MAIN FUNCTION - IMPLEMENTS EACH PHASE
def main():
    global inputImage
    
    #PHASE ONE: UNIFORM AVERAGED TILES & PHASE TWO: UNIFORM AVERAGED TILES WITH BORDERING
    uniformMosaic, uniformBorderMosaic = makeUniformMosaic(inputImage)
    
    
    #PHASE THREE: FEED SubDiv Contours[] as Basis Points for Voronoi Tessellation
    tessellatedMosaic, tessellatedMosaicWithPolyLines = makePolygonalMosaic(inputImage)
    
    Images = []
    
    #Output All To File
    outputFile(uniformMosaic, 0)
    outputFile(uniformBorderMosaic, 1)
    outputFile(tessellatedMosaicWithPolyLines, 2)
    outputFile(tessellatedMosaic, 3)
    
    Images.append(inputImage)
    Images.append(uniformMosaic)
    Images.append(uniformBorderMosaic)
    Images.append(tessellatedMosaicWithPolyLines)
    Images.append(tessellatedMosaic)
    
    Titles = ["Original Image", "uniformMosaic", "uniformBorderMosaic", "tessellatedMosaicWithPolyLines","tessellatedMosaic"]

    for i in range(len(Images)):
        plt.subplot(2, 3, i+1), plt.imshow(cv2.cvtColor(Images[i], cv2.COLOR_BGR2RGB))
        plt.title(Titles[i])
    plt.show()
    
#    end def


#Handle File Input with Error Checking
inputImage = loadFile()
#Call Main :)
main()
