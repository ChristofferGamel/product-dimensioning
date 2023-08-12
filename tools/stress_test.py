import cv2
import numpy as np
import time
from picamera2 import Picamera2
from rembg import remove
import os
from cam import Picture
from contour import Contoured



class Mask():
    def __init__(self) -> None:
        # Image adjustments:
        self.alpha = 1.45          # contrast
        self.beta = -100           # contrast brightness
        self.blocksize = 9         # thresholding
        self.C = 5                 # thresholding
        
        path_to_img = Picture.picture("cam2.jpg")
        print(path_to_img)
        
        self.image = cv2.imread(path_to_img)
        print(self.image)
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]
        self.show()

    def show(self):

        class_init = Contoured()
        contoured = class_init.main(self.image)
        
        while True:           
            cv2.imshow("contoured", contoured)
            
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = Mask()
