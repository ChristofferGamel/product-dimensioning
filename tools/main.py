import cv2
import numpy as np
from picamera2 import Picamera2
from rembg import remove
from cam import Picture
from contour import Contoured



class Mask():
    def __init__(self) -> None:
        # Image adjustments:
        self.alpha = 1.45          # contrast
        self.beta = -100           # contrast brightness
        self.blocksize = 9         # thresholding
        self.C = 5                 # thresholding
        
        cam_0 = Picture.picture("cam0.jpg", 0)
        cam_1 = Picture.picture("cam1.jpg", 1)
        
        image_0 = cv2.imread(cam_0)
        image_1 = cv2.imread(cam_1)
        # print(self.image)
        # self.image_height = self.image.shape[0]
        # self.image_width = self.image.shape[1]
        self.triangulate(image_0, image_1)
        # self.show(image_0)
        # self.show(image_1)

    def triangulate(self, left, right):
        left_image =  Contoured(left)
        left_properties = left_image.properties()
        print(left_properties)
        return

    def show(self, image):
        image = Contoured(image)
        contoured = image.contoured()
        
        while True:           
            cv2.imshow("contoured", contoured)
            
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = Mask()
