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
        self.t_start = time.time()
        # Physical setup
        self.dist = 53.0           # Distance betweeen cameras

        # Image adjustments:
        self.alpha = 1.45          # contrast
        self.beta = -100           # contrast brightness
        self.blocksize = 9         # thresholding
        self.C = 5                 # thresholding

    def take_pictures(self, product_id):
        cam_0 = Picture.picture(0)
        cam_1 = Picture.picture(1)
        pictures = {"id":product_id, "cam_0":cam_0, "cam_1":cam_1}
        return pictures

    def triangulate(self, pictures): 
        self.image_0 = pictures['cam_0']
        self.image_1 = pictures['cam_1']
        product_id = pictures['id']

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
