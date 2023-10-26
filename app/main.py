# Packages
import cv2
import numpy as np
from picamera2 import Picamera2
from rembg import remove
import time

# Files
from cam import Picture
from contour import Contoured
from triangulate import Triangulate
from multithreading import ThreadManager



class Mask():
    def __init__(self) -> None:
        self.t_start = time.time()
        # Physical setup
        self.dist = 53.0           # Distance betweeen cameras

        # Image adjustments:
        self.alpha = 1.45          # contrast
        self.beta = -100           # contrast brightness
        self.blocksize = 9         # thresholding
        self.C = 5                 # thresholding

        # Threading
        self.tm = ThreadManager(2)

    def triangulate(self, product_id):
        cam_0 = Picture.picture(0)
        cam_1 = Picture.picture(1)
        
        self.image_0 = cam_0
        self.image_1 = cam_1

        left = self.image_0
        right = self.image_1
        dist = self.dist

        left_image =  self.tm(left)
        right_image = self.tm(right)

        self.savefig(left_image.contoured(), "left.jpg")
        self.savefig(right_image.contoured(), "right.jpg")

        left = left_image.properties()
        right = right_image.properties()
        
        triangulate = Triangulate()
        width, depth, height = triangulate.object_size(dist, left, right)
        print(f"width: {width}, depth: {depth}, height: {height}")
        
        return_dict = {product_id:{"width":width,"depth":depth,"height":height}}
        t_pictures = time.time()
        print("Time taken: ", t_pictures-self.t_start)
        return return_dict
    
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
