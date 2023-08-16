# Packages
import cv2
import numpy as np
from picamera2 import Picamera2
from rembg import remove

# Files
from cam import Picture
from contour import Contoured
from triangulate import Triangulate



class Mask():
    def __init__(self) -> None:
        # Physical setup
        dist = 53.0                # Distance betweeen cameras


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
        self.triangulate(image_0, image_1, dist)
        # self.show(image_0)
        # self.show(image_1)

    def triangulate(self, left, right, dist):
        left_image =  Contoured(left)
        right_image = Contoured(right)
        self.savefig(left_image.contoured(), "left.jpg")
        self.savefig(right_image.contoured(), "right.jpg")

        left = left_image.properties()
        #left_angle = left["r_angle"]

        right = right_image.properties()
        #right_angle = right["l_angle"]
        triangulate = Triangulate()
        width, depth = triangulate.object_size(dist, left, right)
        print(f"width: {width}, depth: {depth}")
        return
    
    def savefig(self, img, title): # Temporary
        cv2.imwrite(title, img)

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
