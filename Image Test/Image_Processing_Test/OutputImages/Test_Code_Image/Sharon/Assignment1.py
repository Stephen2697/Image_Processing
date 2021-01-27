# Image Processing Assignment 1

# Sharon O'Malley C16469614 DT228 2019
# I will be using image processing techniques to identify and enhance the shark in the image.
# I will be using image processing techniques such as:
# changing the colour space, thresholding, masking, Kernels and cropping


# import the necessary packages:
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
from matplotlib import colors
import easygui

######### Reading Images #########

# Opening an image from a file:
#I = cv2.imread("Shark.png")
I =cv2.imread("Shark 1.png")

######### Colourspaces #########

# Converting to different colour spaces:
RGB = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)

# Seperating the channels in the colour spaces:
Y, U, V = cv2.split(YUV)
R, G, B = cv2.split(RGB)

#### combining colour channels ###
RU = cv2.merge([R, U, U])
new = cv2.cvtColor(RU, cv2.COLOR_BGR2GRAY)

#### Adaptive Threshold to seperate the shark from the background and create a mask of the image ####
B= cv2.adaptiveThreshold(new, maxValue = 255, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType = cv2.THRESH_BINARY_INV, blockSize = 941, C = 2);

#### Morphology ####
shape = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
NewMask = cv2.erode(B, shape)
i = 0
while i < 4:
  NewMask = cv2.morphologyEx(NewMask,cv2.MORPH_OPEN,shape)
  NewMask = cv2.erode(NewMask, shape)
  i += 1

#### Applying the original shark over the mask and changing background of the image to white####
sel = cv2.bitwise_and(I, I, mask = NewMask)
sel[np.where((sel==[0,0,0]).all(axis=2))] = [255, 255, 255]

cv2.imshow("sel", sel)
cv2.waitKey(0)

####Finding X, Y, Height and Width of shark in the image####
light_blue = np.array([4, 3,4]) 
dark_blue = np.array([210, 255, 255])
maskroi = cv2.inRange(sel, light_blue, dark_blue)

## Using more morphology to rid pixels outside of the shark for better identification shark
maskroi = cv2.erode(maskroi, shape)
while i < 9:
  maskroi = cv2.erode(maskroi, shape)
  maskroi = cv2.morphologyEx(maskroi,cv2.MORPH_OPEN,shape)
  i += 1

cv2.imshow("maskroi", maskroi)
cv2.waitKey(0)

## Calculates and returns point x, y, height and width of the shark in the mask
(x,y,w,h) = cv2.boundingRect(maskroi)

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
C = sel[y:h, x:w]

print(x, y, w, h)
cv2.imshow("C", C)
cv2.waitKey(0)

#### Showing the evolution of my images on MatPlotLib####

I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
sel = cv2.cvtColor(sel, cv2.COLOR_BGR2RGB)
Final =  cv2.cvtColor(C, cv2.COLOR_BGR2RGB)
Images = [I, RU, B, NewMask, sel, Final]
Titles = ["Original Image", "Colour Space", "Threshold", "Morphology", "Final Image","Cropped"]

for x in range(6):
	plt.subplot(2, 3, x+1)
	if Titles[x] == "Threshold" or Titles[x] == "Morphology":
		plt.imshow(Images[x], cmap='gray')
	else:
		plt.imshow(Images[x])
	plt.axis("off")
	plt.title(Titles[x])


plt.show() 

#Displaying Final Image
cv2.imshow("Displaying Final Image", C)
key = cv2.waitKey(0)

####Results####
#I attempted using equalisiation on the image before thresholding the image however I did not get the desired results.
#So I decided to remove equalisation. The below code is the code I was using for it.

#H = cv2.equalizeHist(new)
#values1 = H.ravel()

#I then tried to use kernels to blur more of the pixels that were not part of the shark. However, I also did not get the desired results here.
#The code I was attempting to do this with was

#kernel = np.ones((5,5),np.float32)/25
#F = cv2.filter2D(sel,ddepth=-1, kernel = kernel)

#As I was trying to crop the picture accourding to the sharks location, I found the boundingrect function.
#https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=boundingrect
 
