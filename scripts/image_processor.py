import cv2
import math
import numpy as np

class Mask():
    def __init__(self, image_path, image_name, alpha, beta, kernel_iterations, kernel_size, C)-> None:
        # Image properties
        
        self.image = cv2.imread(image_path)
        self.image = self.ResizeWithAspectRatio(self.image, height=700)
        self.image_name = image_name
        self.alpha_v = 0
        self.beta_v = 0
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]

        # Camera properties
        self.camera_angle = 78 #degrees

        # Image adjustments:
        self.alpha = alpha #0.82#2.01#201/100#0.4645669291338583
        self.beta = beta
        self.kernel_iterations = kernel_iterations
        self.kernel_size = kernel_size
        self.C = C

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
        kernel = np.ones((self.kernel_size,self.kernel_size),np.uint8)
        er = cv2.erode(image,kernel,iterations = self.kernel_iterations)
        return er
    
    def contour(self, image):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        image_with_polygon = self.image.copy() 
        try:
            con = self.image.copy() 
            cv2.drawContours(con, contours, 3, (0, 255, 0), 3)
            
            largest_contour = max(contours, key=cv2.contourArea)
            contours_without_largest = [contour for contour in contours if contour is not largest_contour]
            second_largest_contour = max(contours_without_largest, key=cv2.contourArea)
            # print(second_largest_contour)
            self.find_extremes(second_largest_contour)

            
            cv2.line(image_with_polygon, (self.max_x,self.min_y), (self.max_x,self.max_y), (0, 255, 0), 3)
            cv2.line(image_with_polygon, (self.min_x,self.max_y), (self.max_x,self.max_y), (0, 255, 0), 3)
            cv2.line(image_with_polygon, (self.min_x,self.min_y), (self.min_x,self.max_y), (0, 255, 0), 3)
            cv2.line(image_with_polygon, (self.min_x,self.min_y), (self.max_x,self.min_y), (0, 255, 0), 3)
            cv2.drawContours(image_with_polygon, second_largest_contour, -1, (0, 255, 0), thickness=2)
        except:
            pass
        for contour in contours:
            # Approximate the contour with a polygon
            epsilon = 0.14 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Draw the polygon
            cv2.polylines(self.image_copy, [approx], True, (0, 255, 0), 2)
        return image_with_polygon
    
    def find_extremes(self, list):
        self.max_x = 0
        self.max_y = 0
        self.min_y = self.image_height
        self.min_x = self.image_width
        # print(f"Height: {self.image_height}, Width: {self.image_width}")
        
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
    
    def calculate_angle2(self, image_width, point, FOV_x):
        angle_rad = math.atan((2*point/image_width) * FOV_x/image_width)
        angle_deg = self.rad_to_deg(angle_rad)
        return angle_deg
    def calculate_angle_y(self, image_height, point_y, FOV_y):
        angle_rad = math.atan((2 * point_y / image_height - 1) * math.tan(math.radians(FOV_y) / 2))
        angle_deg = math.degrees(angle_rad)
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
    def ResizeWithAspectRatio(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)
    
    def final_image(self):
        
        contrasted = self.contrast(self.image, self.alpha, self.beta)
        thresholded = self.thresholding(contrasted)
        eroded = self.erosion(thresholded)
        contoured = self.contour(eroded)
        while True:
            cv2.imshow(f"{self.image_name}", contoured)
            key = cv2.waitKey(1) & 0xFF

            
            if key == ord("q"):
                break
        cv2.destroyAllWindows()
        return(contoured)
    
    def nothing(self, x):
        pass