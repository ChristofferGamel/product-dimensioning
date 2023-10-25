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



class Mask():
    def __init__(self) -> None:
        t_start = time.time()
        # Physical setup
        self.dist = 53.0                # Distance betweeen cameras


        # Image adjustments:
        self.alpha = 1.45          # contrast
        self.beta = -100           # contrast brightness
        self.blocksize = 9         # thresholding
        self.C = 5                 # thresholding
        
        cam_0 = Picture.picture("cam0.jpg", 0)
        cam_1 = Picture.picture("cam1.jpg", 1)
        
        self.image_0 = cv2.imread(cam_0)
        self.image_1 = cv2.imread(cam_1)

        t_pictures = time.time()
        # print(self.image)
        # self.image_height = self.image.shape[0]
        # self.image_width = self.image.shape[1]
        #self.triangulate(image_0, image_1, dist)
        # self.show(image_0)
        # self.show(image_1)
        #t_triangulate = time.time()
        #print(f"Taking pictures took {t_pictures - t_start} Seconds")
        #print(f"Triangulating took {t_triangulate - t_pictures} Seconds")
        

    def triangulate(self, product_id):
        left = self.image_0
        right = self.image_1
        dist = self.dist

        left_image =  Contoured(left)
        right_image = Contoured(right)

        self.savefig(left_image.contoured(), "left.jpg")
        self.savefig(right_image.contoured(), "right.jpg")

        left = left_image.properties()
        right = right_image.properties()
        
        triangulate = Triangulate()
        width, depth, height = triangulate.object_size(dist, left, right)
        print(f"width: {width}, depth: {depth}, height: {height}")
        
        return_dict = {product_id,{"width":width,"depth":depth,"height":height}}
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
