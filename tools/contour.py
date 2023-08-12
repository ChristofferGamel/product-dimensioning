import cv2
import numpy as np
from matplotlib import pyplot as plt
from rembg import remove


class Contoured():
    def __init__(self) -> None:
        # Image properties
        self.alpha = 1.45           # contrast
        self.beta = -100            # contrast brightness
        self.blocksize = 9          # thresholding
        self.C = 5                  # thresholding

    def contrast(self, image):
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
            # here we are ignoring first counter because
            # findContours function detects whole image as shape
            if i == 0:
                i = 1
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            boxes.append([x, y, x + w, y + h])

        boxes = np.asarray(boxes)
        left, top = np.min(boxes, axis=0)[:2]
        right, bottom = np.max(boxes, axis=0)[2:]

        return left, top, right, bottom
    
    def draw_points_box(self, original_image, x1, y1, x2, y2):
        copy = original_image.copy()
        return cv2.rectangle(copy, (x1, y1), (x2, y2), (0, 255, 0), 5)  
    
    def main(self, image):
        self.image = image

        self.image_height = image.shape[0]
        self.image_width = image.shape[1]
        
        contrasted = self.contrast(image)
        removed_bg = self.remove_bg(contrasted)
        thresholded = self.thresholding(removed_bg)
        
        y1, y2, x1, x2 = self.extreme_points(thresholded)
        draw = self.draw_points_box(self.image, y1, y2, x1, x2)

        return draw