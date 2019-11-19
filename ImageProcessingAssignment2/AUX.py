
#lab = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
#cv2.imshow("lab", lab)
#cv2.waitKey(0)
#luv = cv2.cvtColor(src, cv2.COLOR_BGR2LUV)
#cv2.imshow("luv", luv)
#cv2.waitKey(0)
#xyz = cv2.cvtColor(src, cv2.COLOR_BGR2XYZ)
#cv2.imshow("xyz", xyz)
#cv2.waitKey(0)

#Images = [src, hsv, lab, luv, xyz]
#Titles = ["Original Image", "DST", "LAB", "LUV", "XYZ"]
#
#for x in range(6):
#	plt.subplot(2, 3, x+1)
##	if Titles[x] == "Threshold" or Titles[x] == "Morphology":
##		plt.imshow(Images[x], cmap='gray')
##	else:
#	plt.imshow(Images[x])
#	plt.axis("off")
#	plt.title(Titles[x])
#plt.show()

#testColourChannelInput(src)
#testColourChannelInput(src2)
#testColourChannelInput(src3)


#Adaptive Threshold stuff
#cv2.createTrackbar("Blocksize", WINDOW_NAME, threshold, 255, adjustBlocksize)
#cv2.createTrackbar("Offset", WINDOW_NAME, threshold, 255, adjustOffset)

#src2 = cv2.imread(FILE_LOC)

FILE_NAME = FILE_NAME_ARRAY[0]
FILE_LOC = FILE_PATH + FILE_NAME


FILE_NAME = FILE_NAME_ARRAY[1]
FILE_LOC = FILE_PATH + FILE_NAME

#Blocksize cant be even
if (blockSize > 1 and (blockSize%2==0)):
	blockSize -= 110
