#Created By: © Stephen Alger

import sys
print("Python Version: [" + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "]")


#computer vision library
import cv2

#numerical python library
import numpy as np

#MatPlotLib import - throws
import matplotlib
matplotlib.use("TkAgg")

from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui



loadedImage = cv2.imread("Image.jpeg")
#cv2.imwrite("duplicate.jpeg", loadedImage)
#cv2.imshow("Your Image Window", loadedImage)
#key = cv2.waitKey(0)

loadedImage = cv2.cvtColor(loadedImage, cv2.COLOR_BGR2RGB)
plt.imshow(loadedImage)
plt.show()

def test():
    print("Hello Xcode")
    
test()
