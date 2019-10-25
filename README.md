# ObjectContourExtraction .py [v1.5]

### How to Run Script - Note Args Format:

```sh
$ cd ImageProcessing
--Run This Script as Follows [ObjectExtraction.py] ['FileName.fileExtension']
$ python3 ObjectContourExtraction.py 'Shark 1.PNG'
```

python 3 [ObjectExtraction.py] ['FileName.fileExtension']
Example: python3 ObjectContourExtraction.py 'Shark 1.PNG'

### Design Notes:
- Processing Techniques Implemented: 
-Histogram Equalisation: (Contrast Adjustments)
-Colour Space Manipulation (BGR->HSV): Using the 'V' - brightness value
-Thresholding: Global Binary Thresholding (Not Adaptive Thresh By Design)
-Followed by Contouring to identify all the contours in the image and we select the largest contours as our subject.

- Other Notes: 
-User input - there is use of ‘cv2.waitKey(0)’ statements to allow user control
-The User is in control here, I designed this program to be as ‘hardcode’ independent as possible with sliders for threshold arguments
-Tested on Python 3.7.2 - Mac OS Catalina (Not Compatible with Python 2.7)

### For Best Object Extraction Results try the following values on the slider screen:
- From Testing: Shark 1.png works best @ Thresh=97, Equalised= TRUE, Gaussian Blur = 39
- From Testing: Shark 2.png works best @ Thresh=103, Equalised= TRUE, Gaussian Blur = 38

### Temporary Removals from Code
- Jpeg handling to be re-added (PNG Only at the moment)
- GUI Image selector w/ easygui would be ideal but removed due to bugs

### Known Issues/ Points of Improvement (Non-Exhaustive) :
- More error handling required around cv2 imreads and imwrites
- Allow User to choose between largest Contours in image so they can select a smaller object in the photo not just the largest subjects of the photo.



