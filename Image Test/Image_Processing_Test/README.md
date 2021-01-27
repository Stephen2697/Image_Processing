# Mosaics.py [v1.0]
### Creators: Stephen Alger C16377163 & Chris Clarke C16398141
### How to Run Script:

```sh
$ cd /MosaicsProject
$ python3 Mosaics.py 
```

### Design Notes:
- Mosaic Techniques Implemented: 
-Uniform Tiles with & without Tile Bordering
-Polygonal Tiles built from Thresholding, Contours points and Voronoi Algorithm
-File Input Is handled in the Code, select filename from array of Sample File Names or add your own.

- Other Notes: 
-User input - there is use of ‘cv2.waitKey(0)’ statements to allow user control
-The User is in control here, I designed this program to be as ‘hardcode’ independent as possible with sliders for threshold arguments
-Tested on Python 3.7.2 - Mac OS Catalina & Windows 10 (Not Compatible with Python 2.7) 

### For Best Object Extraction Results try the following values on the slider screen:
- From Testing: Shark 1.png works best @ Thresh=97, Equalised= TRUE, Gaussian Blur = 39
- From Testing: Shark 2.png works best @ Thresh=103, Equalised= TRUE, Gaussian Blur = 38

### Removals from Code
- Delaunay Triangulation - No initial benefit over Voronoi Polygonals
