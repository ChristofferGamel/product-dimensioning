import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('./tools/monster.jpg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
# global thresholding
ret1,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# Otsu's thresholding
ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
blur = cv.GaussianBlur(img,(5,5),0)
ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# plot all the images and their histograms
while True:
    #cv.imshow("th1", th1)
    #cv.imshow("th2", th2)
    cv.imshow("th3", th3)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
        
cv.destroyAllWindows()