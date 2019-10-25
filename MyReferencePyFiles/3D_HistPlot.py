#!/usr/local/bin/python3
#Creator: Stephen Alger
#Date 20-OCT-2019
#3D Histogram plotting Python HSV 

#Import Stuff...
import sys, os, cv2, numpy as np, matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

image_Colour = cv2.imread('Shark 1.png')
image_ColourRGB = cv2.cvtColor(image_Colour, cv2.COLOR_BGR2RGB)
image_ColourHSV = cv2.cvtColor(image_ColourRGB, cv2.COLOR_RGB2HSV)

h, s, v = cv2.split(image_ColourHSV)
fig = plt.figure()
axis = fig.add_subplot(1, 1, 1, projection="3d")

pixel_colors = image_ColourRGB.reshape((np.shape(image_ColourRGB)[0]*np.shape(image_ColourRGB)[1], 3))
norm = colors.Normalize(vmin=-1.,vmax=1.)
norm.autoscale(pixel_colors)
pixel_colors = norm(pixel_colors).tolist()


axis.scatter(h.flatten(), s.flatten(), v.flatten(), facecolors=pixel_colors, marker=".")
axis.set_xlabel("Hue")
axis.set_ylabel("Saturation")
axis.set_zlabel("Value")
plt.show()
