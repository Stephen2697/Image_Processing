#My OpenCV Cheatsheet

#Import
src = cv2.imread(FILE_LOC)

#Show Image
cv2.imshow("Post Erosion Phase", erosionPhase)
cv2.waitKey(0)

#Export
FILE_LOC = FILE_OUT_PATH + FILE_OUT_NAME
print("Your Extraction Image Has Been Saved To File @ [" + FILE_LOC + "]")
cv2.imwrite(FILE_LOC, dst)

#Convert Colour
dst = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

#Split Colours
hue,saturation,brightness = cv2.split(dst)

#Equalise 
tempMatrix = cv2.equalizeHist(tempMatrix)

#Threshold - All Types
ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
ret,thresh2 = cv.threshold(img,127,255,cv.THRESH_BINARY_INV)
ret,thresh3 = cv.threshold(img,127,255,cv.THRESH_TRUNC)
ret,thresh4 = cv.threshold(img,127,255,cv.THRESH_TOZERO)
ret,thresh5 = cv.threshold(img,127,255,cv.THRESH_TOZERO_INV)
thresh6 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,2)
thresh7 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)

# Otsu's thresholding
otsuVal1,thresh8 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
blur = cv.GaussianBlur(img,(5,5),0)
otsuVal2,thresh9 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)


titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV','Adaptive','Ad-Gauss','Otsu', 'OtsuBlur']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5,thresh6,thresh7,thresh8,thresh9]

for i in range(9):
    plt.subplot(3,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

#Contour
contours, _ = cv2.findContours(tempMatrix,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#Draw Contour & Sort
cv2.drawContours(ballSelectionMask, contours, largest, colour, cv2.FILLED)

for i in range(len(contours)):
    dimension = len(contours[i])
    if (dimension > maxDimension):
        maxDimension = dimension
        largest = i

#Rect
cv2.rectangle(ballSelectionMask,(x,y),(x+w,y+h),(255,255,255), cv2.FILLED)
x,y,w,h = cv2.boundingRect(contours[largest])

#Hough Circles
circles = cv2.HoughCircles(ballSelectionMask,cv2.HOUGH_GRADIENT,2,200,param1=20,param2=10,minRadius=int(w*.25),maxRadius=int(w/2))

#Crop to Mask

#Bitwise Operations on Masks
def bitwiseAND(mask1, mask2):
    return (cv2.bitwise_and(mask1, mask2))
    
def bitwiseNOT(mask1, mask2):
    return (cv2.bitwise_not(mask1, mask2))

def bitwiseOR(mask1, mask2):
    return (cv2.bitwise_or(mask1, mask2))
    
def bitwiseXOR(mask1, mask2):
    return (cv2.bitwise_xor(mask1, mask2))

#Invert Colours B->W
gray = cv2.cvtColor(subMask, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 15, cv2.THRESH_BINARY)
cv2.imshow("Post Background Invert", thresh)
subMask[thresh == 0] = 255

#Use Razors - Ellip/ Rect/ Open/ Close etc
razor = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
erosionPhase = cv2.erode(subMask, razor, iterations = 1)
cv2.imshow("Post Erosion Phase", erosionPhase)
cv2.waitKey(0)

#FUNCTION TO APPLY CV DIALTION ON BALL - CODE PREVIOUSLY USED, IS NOT USED AT SUBMISSION
def morphology_dialate(ballSelectionMask):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    ballSelectionMask = cv2.dilate(ballSelectionMask, kernel, iterations=3)
    cv2.imshow("DIALATE",ballSelectionMask)
    cv2.waitKey(delay = 0)
    return ballSelectionMask
