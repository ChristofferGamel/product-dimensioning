import cv2
import numpy as np
from matplotlib import pyplot as plt
from rembg import remove
import math


class Contoured():
    def __init__(self, image) -> None:
        # Image properties
        self.image = image
        self.alpha = 1.45           # contrast
        self.beta = -100            # contrast brightness
        self.blocksize = 9          # thresholding
        self.C = 5                  # thresholding

        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]

        # Camera properties
        self.horizontal_fov = 66 #degrees
        self.vertical_fov = 41 #degrees

        # self.contoured()
    
    def __abs__(self):
        return self.string

    def contrast(self, image):
        print(type(image))
        contrast = cv2.convertScaleAbs(image, alpha=self.alpha, beta=self.beta)
        return contrast
    
    def remove_bg(self, image):
        removed_bg = remove(image)
        return removed_bg
    
    def thresholding(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_8bit = cv2.convertScaleAbs(gray)
        th2 = cv2.adaptiveThreshold(gray_8bit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.blocksize, self.C)
        return th2
    
    def extreme_points(self, binary_image):
        # Find the contours of the object
        contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        i = 0
        for c in contours:
            # here we are ignoring the first contour because
            # findContours function detects the whole image as a shape
            if i == 0:
                i = 1
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            boxes.append([x, y, x + w, y + h])

        boxes = np.asarray(boxes)
        boxes = [] # DELETE 
        if len(boxes) == 0:
            raise Exception("boxes len = 0")


        left, top = np.min(boxes, axis=0)[:2]
        right, bottom = np.max(boxes, axis=0)[2:]
        
        self.left, self.top, self.right, self.bottom = left, top, right, bottom

        return left, top, right, bottom
    
    def draw_points_box(self, original_image, x1, y1, x2, y2):
        copy = original_image.copy()
        return cv2.rectangle(copy, (x1, y1), (x2, y2), (0, 255, 0), 5) 
    
    def deg_to_rad(self, deg):
        return((deg * math.pi)/180)
    def rad_to_deg(self, rad):
        return(rad*(180/math.pi))
    
    def angle(self, point, fov, image_width):
        if(point == image_width/2): # Division by zero prevention
            return 0
        B = fov/2
        b = image_width/2

        C_rad = math.radians(B)
        b__1 = b / math.tan(C_rad)  
        a =  abs(point - b)
        angle = math.atan(b__1/a)
        angle_deg = math.degrees(angle) 
        if(point>b):
            return 0 - (90 - angle_deg)
        else:
            return 90 - angle_deg

    
    def properties(self):
        dict = {"image_width":self.image_width, 
                "image_height":self.image_height,
                "left":self.left,
                "top":self.top,
                "right":self.right,
                "bottom":self.bottom,
                "horizontal_fov":self.horizontal_fov,
                "vertical_fov":self.vertical_fov,
                "l_angle":self.angle(self.left, self.horizontal_fov, self.image_width),
                "r_angle":self.angle(self.right, self.horizontal_fov, self.image_width),
                "top_angle":self.angle(self.top, self.vertical_fov, self.image_height),
                "bottom_angle":self.angle(self.bottom, self.vertical_fov, self.image_height)}
        return dict 
    
    
    
    def contoured(self):        
        contrasted = self.contrast(self.image)
        removed_bg = self.remove_bg(contrasted)
        thresholded = self.thresholding(removed_bg)
        
        try:
            y1, y2, x1, x2 = self.extreme_points(thresholded)
        except:
            raise Exception("No contours found")
        draw = self.draw_points_box(self.image, y1, y2, x1, x2)

        return draw
