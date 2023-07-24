import cv2
import numpy as np
import math


class Mask():
    def __init__(self, image_path, orientation) -> None:
        # Image properties
        self.orientation = orientation
        self.image = cv2.imread(image_path)
        self.alpha_v = 0
        self.beta_v = 0
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]

        # Camera properties
        self.camera_angle = 78 #degrees
        self.distance_to_object = 35.5 #cm
        self.camera_height = 10 #cm

        self.final_image()

    def contrast(self, image, alpha, beta): #0.8110236220472441, 100
        contrast = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return contrast
    
    def thresholding(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_8bit = cv2.convertScaleAbs(gray)
        th2 = cv2.adaptiveThreshold(gray_8bit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
        return th2

    def erosion(self, image):
        kernel = np.ones((4,4),np.uint8)
        er = cv2.erode(image,kernel,iterations = 2)
        return er
    
    def contour(self, image):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        
        con = self.image.copy() 
        cv2.drawContours(con, contours, 3, (0, 255, 0), 3)
        
        largest_contour = max(contours, key=cv2.contourArea)
        contours_without_largest = [contour for contour in contours if contour is not largest_contour]
        second_largest_contour = max(contours_without_largest, key=cv2.contourArea)
        # print(second_largest_contour)
        self.find_extremes(second_largest_contour)

        image_with_polygon = self.image.copy() 
        cv2.line(image_with_polygon, (self.max_x,self.min_y), (self.max_x,self.max_y), (0, 255, 0), 3)
        cv2.line(image_with_polygon, (self.min_x,self.max_y), (self.max_x,self.max_y), (0, 255, 0), 3)
        cv2.line(image_with_polygon, (self.min_x,self.min_y), (self.min_x,self.max_y), (0, 255, 0), 3)
        cv2.line(image_with_polygon, (self.min_x,self.min_y), (self.max_x,self.min_y), (0, 255, 0), 3)
        cv2.drawContours(image_with_polygon, second_largest_contour, -1, (0, 255, 0), thickness=2)
        
        return image_with_polygon
    
    def find_extremes(self, list):
        self.max_x = 0
        self.max_y = 0
        self.min_y = self.image_height
        self.min_x = self.image_width
        print(f"Height: {self.image_height}, Width: {self.image_width}")
        
        for m_x in range(len(list)):
            if(list[m_x][0][0] > self.max_x):
                self.max_x = list[m_x][0][0]
                self.max_x_set = list[m_x][0]
        for m_y in range(len(list)):
            if(list[m_y][0][1] > self.max_y):
                self.max_y = list[m_y][0][1]
                self.max_y_set = list[m_y][0]

        for mi_y in range(len(list)):
            if list[mi_y][0][1] < self.min_y:
                self.min_y = list[mi_y][0][1]
                self.min_y_set = list[mi_y][0]
        for mi_x in range(len(list)):
            if list[mi_x][0][0] < self.min_x:
                self.min_x = list[mi_x][0][0]
                self.min_x_set = list[mi_x][0]



        # print("Max x set: ",self.max_x_set)
        # print("Max y set: ",self.max_y_set)
        # print("Min x set: ",self.min_x_set)
        # print("min y set: ",self.min_y_set)
    
    def angle(self):
        if self.orientation=="l": #left maxima
            distance_pixels = self.max_x_set[0]
            angle = (distance_pixels/self.image_width) * self.camera_angle

        elif self.orientation=="r": #right maxima
            distance_pixels = self.min_x_set[0]
            angle = (distance_pixels/self.image_width) * self.camera_angle
        
        return(angle)
    
    def final_image(self):
        contrasted = self.contrast(self.image, 0.4645669291338583, 38)
        thresholded = self.thresholding(contrasted)
        eroded = self.erosion(thresholded)
        contoured = self.contour(eroded)
        return(contoured)
    
    def nothing(self, x):
        pass

class Dimensions():
    def __init__(self) -> None:
        left_path = "./captured_images/left.jpg"
        right_path = "./captured_images/right.jpg"
        self.left_properties = Mask("./captured_images/left.jpg", "l")
        self.right_properties = Mask("./captured_images/right.jpg", "r")
        self.object_cam_angle_left = self.left_properties.angle()
        self.object_cam_angle_right = self.right_properties.angle()
        self.triangulate()


        pass

    def triangulate(self):
        angle_rel = (180 - self.left_properties.camera_angle) / 2 #83.28333333333333
        
        self.object_cam_angle_left = self.left_properties.angle()
        left_angle_rel = 180 - self.object_cam_angle_left - angle_rel
        print(left_angle_rel)

        self.object_cam_angle_right = self.right_properties.angle()
        right_angle_rel = 90 - (self.right_properties.camera_angle/2) + self.object_cam_angle_right
        print(right_angle_rel)
        return



if __name__ == "__main__":
    app = Dimensions()
