import cv2
import numpy as np
import math
from trianglesolver import solve, degree




class Mask():
    def __init__(self, image_path) -> None:
        # Image properties
        
        self.image = cv2.imread(image_path)
        self.alpha_v = 0
        self.beta_v = 0
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]

        # Camera properties
        self.camera_angle = 78 #degrees

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



        print("Max x set: ",self.max_x_set)
        print("Max y set: ",self.max_y_set)
        print("Min x set: ",self.min_x_set)
        print("min y set: ",self.min_y_set)
    
    def angle(self, orientation): # angle from leftmost fov to r or l edge
        if orientation=="l": #left edge of image
            distance_pixels = self.min_x_set[0]
            angle = (distance_pixels/self.image_width) * self.camera_angle

        elif orientation=="r": #right edge of image
            distance_pixels = self.max_x_set[0]
            angle = (distance_pixels/self.image_width) * self.camera_angle
        elif orientation=="test":
            object_center_x = self.max_x_set[0] - self.min_x_set[0]
            angle = self.calculate_angle(self.image_width, object_center_x, 360, self.camera_angle)
        
        return(angle)
    def calculate_angle(self, image_width, point, image_center_x, FOV_x):
        angle_rad = math.atan((point - image_center_x) * math.tan(self.rad_to_deg(FOV_x) / 2) / (image_width / 2))
        angle_deg = self.rad_to_deg(angle_rad)
        return angle_deg
    def rad_to_deg(self, rad):
        return(rad*(180/math.pi))
    def deg_to_rad(self, deg):
        return((deg * math.pi)/180)
    def properties(self):
        dict = {"image_width":self.image_width, 
                "image_height":self.image_height,
                "y_min_set":self.min_y_set,
                "x_min_set":self.min_x_set,
                "y_max_set":self.max_y_set,
                "x_max_set":self.max_x_set,
                "cam_fov":self.camera_angle}
        return dict
    
    def final_image(self):
        contrasted = self.contrast(self.image, 0.4645669291338583, 38)
        thresholded = self.thresholding(contrasted)
        eroded = self.erosion(thresholded)
        contoured = self.contour(eroded)
        while True:
            cv2.imshow("contoured", contoured)
            key = cv2.waitKey(1) & 0xFF

            
            if key == ord("q"):
                break
        cv2.destroyAllWindows()
        return(contoured)
    
    def nothing(self, x):
        pass

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

class Dimensions():
    def __init__(self) -> None:
        left_path = "./captured_images/left.jpg"
        right_path = "./captured_images/right.jpg"
        self.left_properties = Mask("./captured_images/left.jpg") #front
        self.right_properties = Mask("./captured_images/right.jpg") #side
        
        self.common_point()
        self.width()
    
    def positive(self,num):
        return (math.sqrt((num)**2))


    def common_point(self):
        # Image properties:
        dist_betw_cams = 40.54
        self.left_image_properties = self.left_properties.properties()
        self.right_image_properties = self.right_properties.properties()
        print("l/r")

        self.left_image_width = self.left_image_properties["image_width"]
        self.right_image_width = self.right_image_properties["image_width"]
        print("l/r: Width:",self.left_image_width, self.right_image_width)
        
        self.left_center = self.left_image_width / 2
        self.right_center = self.right_image_width / 2
        print("l/r: Center:",self.left_center, self.right_center)
        
        
        self.left_fov = self.left_image_properties["cam_fov"]
        self.right_fov = self.right_image_properties["cam_fov"]
        print("l/r FOV: ",self.left_fov,self.right_fov)

        # Contoured values
        self.left_cam_min_x = self.left_image_properties["x_min_set"][0]
        self.left_cam_max_x = self.left_image_properties["x_max_set"][0]
        print("left_max: ",self.left_cam_max_x)


        self.right_cam_min_x = self.right_image_properties["x_min_set"][0]
        self.right_cam_max_x = self.right_image_properties["x_max_set"][0]
        print("right_min: ",)

        

        # Angles
        left_cam_angle_to_right_point = self.left_properties.calculate_angle(self.left_image_width, self.left_cam_max_x, self.left_center, self.left_fov)
        right_cam_angle_to_left_point = self.right_properties.calculate_angle(self.right_image_width, self.right_cam_min_x, self.right_center, self.right_fov)

        A = 90 - 45 - math.sqrt((left_cam_angle_to_right_point)**2)
        B = 90 - 45 - math.sqrt((right_cam_angle_to_left_point)**2)
        print("ab: ",left_cam_angle_to_right_point,right_cam_angle_to_left_point)
        c = 40.54

        a,b,c,A,B,C = solve(c=c, A=A*degree, B=B*degree)
        self.b = b

        print(a,b)

    def width(self): # front / left camera
        image_properties = self.left_properties.properties()
        right = self.left_properties.calculate_angle(self.left_image_width, self.left_cam_max_x, self.left_center, self.left_fov)
        left = self.left_properties.calculate_angle(self.left_image_width, self.left_cam_min_x, self.left_center, self.left_fov)
        object_angle = self.positive(right) + self.positive(left)

        # Method 1 assuming orthogonal placement of object
        C = object_angle
        A = (180 - object_angle)/2
        B = (180 - object_angle)/2
        b = self.b

        a,b,c,A,B,C = solve(C=C*degree,B=B*degree,b=b)
        print(c/2)

        


    def depth(self): # length
        return    
    
    def height(self):
        return
    def deg_to_rad(self, deg):
        return((deg * math.pi)/180)



if __name__ == "__main__":
    app = Dimensions()
