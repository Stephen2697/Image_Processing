#!/usr/local/bin/python3
#Creator: Stephen Alger
#Date 15-OCT-2019
#Advanced Threshold Segmentation Implementation

#Import Stuff...
import sys, os, cv2, numpy as np, matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

BLOCKSIZE = 11
C_CONSTANT = 3

image = cv2.imread('Shark 1.png', cv2.IMREAD_GRAYSCALE)

image_Colour = cv2.imread('Shark 1.png')
image_ColourRGB = cv2.cvtColor(image_Colour, cv2.COLOR_BGR2RGB)
image_ColourHSV = cv2.cvtColor(image_ColourRGB, cv2.COLOR_RGB2HSV)
image_ColourLAB= cv2.cvtColor(image_Colour, cv2.COLOR_BGR2LAB)

red ,green,blue = cv2.split(image_ColourRGB)
h,s,v = cv2.split(image_ColourHSV)
l,a,b = cv2.split(image_ColourLAB)

image_EQB = cv2.equalizeHist(blue)
filename = 'EQB-Shark1.png'
cv2.imwrite(filename, image_EQB)


#---------Hist Check

#hist = cv2.calcHist([image_Colour],[0],None,[256],[0,256])
#plt.plot(hist)
#plt.show()

#----------EQ Check

filename = 'EQ-Shark1.png'
image_EQ = cv2.equalizeHist(image)
cv2.imwrite(filename, image_EQ)

#--------Get AdaptiveThresholdMean
adaptMean = cv2.adaptiveThreshold(image_EQB,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,11)
adaptMean = cv2.adaptiveThreshold(adaptMean,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,1)
adaptMean = cv2.bitwise_not(adaptMean)

#--------Erosion - remove blobs (opening = erosion then dilation)

shapeRect = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
#shapeEllip = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

def shapeEllipSize(x):
	shapeEllip = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(x),int(x)))
	return shapeEllip

shapeSize = 5
erodedMasklvl1 = cv2.erode(adaptMean,shapeEllipSize(shapeSize))

#for i in range(2):
#	erodedMask = cv2.erode(erodedMask,shapeEllipSize(shapeSize))
#	shapeSize /= 3
#
mergeMask = cv2.bitwise_and(src1 = adaptMean, src2 = erodedMasklvl1)
maskArr = [adaptMean, erodedMasklvl1, mergeMask]

#for i in range(3):
#    plt.subplot(1,3,i+1), plt.imshow(maskArr[i], "gray")
#
#plt.show()

#NewMask1a= cv2.morphologyEx(OldMask,cv2.MORPH_OPEN,shapeRect)

#-------Dilation - fill gaps & smooth bound (closing = dilation then erosion)
#NewMask2= cv2.dilate(adaptMean,shape)
#NewMask2a = cv2.morphologyEx(OldMask,cv2.MORPH_CLOSE,shape)
dilatedMask = cv2.dilate(erodedMasklvl1,shapeEllipSize(2))
shapeSize = 21
#for i in range(3):
#	dilatedMask = cv2.dilate(dilatedMask,shapeEllipSize(shapeSize))
#	shapeSize /= 1

maskArr = [adaptMean, erodedMasklvl1, dilatedMask]
#
#for i in range(3):
#    plt.subplot(1,3,i+1), plt.imshow(maskArr[i], "gray")
#
#plt.show()

#-------Boundary Extract
#Boundary = cv2.morphologyEx(mask,cv2.MORPH_GRADIENT,shape)
#---------Edge Detection



#sel = cv2.bitwise_or(src1 = image_EQ, src2 = adaptMean)
#sel2 = cv2.bitwise_and(src1 = sel, src2 = adaptMean)


#ret1, thresh1 = cv2.threshold(sel2,200,255, cv2.THRESH_BINARY)
#cv2.imshow(winname = "selected", mat = sel2)
#cv2.waitKey(delay = 0)

#plt.subplot(1,1,1), plt.imshow(tresh, "gray")
#plt.show()

edgeEQ = cv2.Canny(image = adaptMean, threshold1 = 245, threshold2 = 255)

#sel3 = cv2.bitwise_xor(src1 = sel, src2 = edgeEQ)
#cv2.imshow(winname = "selected", mat = sel3)
#cv2.waitKey(delay = 0)

edgeAdaptEQ = cv2.Canny(image = adaptMean, threshold1 = 225, threshold2 = 230)

#plt.subplot(1,1,1), plt.imshow(adaptMean, "gray")
#plt.show()
#
#plt.subplot(1,1,1), plt.imshow(edgeEQ, "gray")
#plt.show()

titlesEdge = ['r','g','b','l','a', 'b', 'h','s','v']
imageEdges = [red, green,blue, l,a,b,h,s,v]

for i in range(9):
    plt.subplot(3,3,i+1), plt.imshow(imageEdges[i], "RGB")

    plt.title(titlesEdge[i])
plt.show()

#---------Thresholding

#ret,thresh = cv2.threshold(image_EQ,127,255,cv2.THRESH_BINARY)
#
#image1 = cv2.medianBlur(image_EQ,5)
#ad1 = cv2.adaptiveThreshold(image1,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,255,11)
#ad2 = cv2.adaptiveThreshold(image1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,255,11)
#
#blur = cv2.GaussianBlur(image_EQ,(5,5),0)
#ret1, OTSU = cv2.threshold(blur,120,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#---------


#titles = ['Before','EQ', 'Global','Ad-Mean','Ad-Gaussian', 'otsu']
#images = [image, image_EQ, thresh, ad1, ad2, OTSU]
#
#for i in range(6):
#    plt.subplot(2,3,i+1), plt.imshow(images[i], "gray")
#
#    plt.title(titles[i])
#plt.show()



