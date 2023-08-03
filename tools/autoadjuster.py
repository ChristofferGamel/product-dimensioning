import cv2
import numpy as np
import math
from trianglesolver import solve, degree
from right_triangle import RightTriangle
import time




class Mask():
    def __init__(self, image_path, image_name, alpha, beta, kernel_iterations, kernel_size, C)-> None:
        # Image properties
        
        self.image = cv2.imread(image_path)
        self.image_name = image_name
        self.alpha_v = 0
        self.beta_v = 0
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]

        # Camera properties
        self.camera_angle = 78 #degrees

        # Image adjustments:
        self.alpha = alpha
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
    
    def final_image(self):
        contrasted = self.contrast(self.image, self.alpha, self.beta)
        thresholded = self.thresholding(contrasted)
        eroded = self.erosion(thresholded)
        contoured = self.contour(eroded)
        # while True:
        #     cv2.imshow(f"{self.image_name}", contoured)
        #     key = cv2.waitKey(1) & 0xFF

            
        #     if key == ord("q"):
        #         break
        # cv2.destroyAllWindows()
        return(contoured)
    
    def nothing(self, x):
        pass

#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

class Dimensions():
    def __init__(self) -> None:
        self.main()

   
    
    def positive(self,num):
        return (math.sqrt((num)**2))
    
    def min_y(self):
        self.left_image_properties = self.left_properties.properties()
        return self.left_image_properties["y_min_set"][1]
    def max_y(self):
        self.left_image_properties = self.left_properties.properties()
        return self.left_image_properties["y_max_set"][1]
    def min_x(self):
        self.left_image_properties = self.left_properties.properties()
        return self.left_image_properties["x_min_set"][0]
    def max_x(self):
        self.left_image_properties = self.left_properties.properties()
        return self.left_image_properties["x_max_set"][0]
    

    def common_point(self):
        # Image properties:
        dist_betw_cams = 70.1
        self.left_image_properties = self.left_properties.properties()
        self.right_image_properties = self.right_properties.properties()
        # print("l/r")

        self.left_image_width = self.left_image_properties["image_width"]
        self.right_image_width = self.right_image_properties["image_width"]
        # print("l/r: Width:",self.left_image_width, self.right_image_width)
        
        self.left_center = self.left_image_width / 2
        self.right_center = self.right_image_width / 2
        # print("l/r: Center:",self.left_center, self.right_center)
        
        
        self.left_fov = self.left_image_properties["cam_fov"]
        self.right_fov = self.right_image_properties["cam_fov"]
        # print("l/r FOV: ",self.left_fov,self.right_fov)

        # Contoured values
        self.left_cam_min_x = self.left_image_properties["x_min_set"][0]
        self.left_cam_max_x = self.left_image_properties["x_max_set"][0]
        # print("left_max: ",self.left_cam_max_x)


        self.right_cam_min_x = self.right_image_properties["x_min_set"][0]
        self.right_cam_max_x = self.right_image_properties["x_max_set"][0]
        # print("right_min: ",)

        
        # Angles
        left_cam_angle_to_right_point = self.left_properties.calculate_angle2(self.left_image_width, self.left_cam_max_x, self.left_fov)
        right_cam_angle_to_left_point = self.right_properties.calculate_angle2(self.right_image_width, self.right_cam_min_x, self.right_fov)

        A = 90 - 45 - math.sqrt((left_cam_angle_to_right_point)**2)
        B = 90 - 45 - math.sqrt((right_cam_angle_to_left_point)**2)
        # print("ab: ",left_cam_angle_to_right_point,right_cam_angle_to_left_point)
        c = dist_betw_cams

        a,b,c,A,B,C = solve(c=c, A=A*degree, B=B*degree)
        self.b = b

        # print(a,b)

    def width(self): # front / left camera
        image_properties = self.left_properties.properties()
        right = self.left_properties.calculate_angle2(self.left_image_width, self.left_cam_max_x, self.left_fov)
        left = self.left_properties.calculate_angle2(self.left_image_width, self.left_cam_min_x, self.left_fov)
        object_angle = self.positive(right) + self.positive(left)

        # Method 1 assuming orthogonal placement of object
        C = object_angle
        A = 90 - self.positive(right)
        B = 90 - self.positive(left)
        b = self.b
        # print(f"C: {C}, A: {A}, B: {B}, b:{b}")

        a,b,c,A,B,C = solve(C=C*degree,B=B*degree,b=b)
        self.triangle_height = math.sin(A)*b

        # print(c)
        self.object_width = c
        return c

    def depth(self): # length
        image_properties = self.right_properties.properties()
        right = self.right_properties.calculate_angle2(self.right_image_width, self.right_cam_max_x, self.right_fov)
        left = self.left_properties.calculate_angle2(self.right_image_width, self.right_cam_min_x, self.right_fov)
        object_angle = self.positive(right) + self.positive(left)

        # Method 1 assuming orthogonal placement of object
        C = object_angle
        A = 90 - self.positive(right)
        B = 90 - self.positive(left)
        b = self.b
        # print(f"C: {C}, A: {A}, B: {B}, b:{b}")

        a,b,c,A,B,C = solve(C=C*degree,B=B*degree,b=b)
        # print("depth: ",c)
        self.object_depth = c
        return c
          
    
    def height(self): # 
        dist_to_center = self.triangle_height
        max_y = self.left_image_properties["y_max_set"][1]
        min_y = self.left_image_properties["y_min_set"][1]
        height = self.left_image_properties["image_height"]
        center = height/2
        angle1 = self.left_properties.calculate_angle_y(height, max_y, self.left_fov)
        angle2 = self.left_properties.calculate_angle_y(height, min_y, self.left_fov)
        
        angle_sum = self.positive(angle1) + self.positive(angle2)   
        
        return
    def deg_to_rad(self, deg):
        return((deg * math.pi)/180)
    def call(self, alpha, beta, kernel_i, kernel_size, C):
        left_path = "./captured_images/ss7650ISO100.jpg"
        right_path = "./captured_images/right.jpg"
        # beta = 48
        # kernel_i = 2
        # kernel_size = 4
        # C = 4
        self.left_properties = Mask(left_path, "Left", alpha/100, beta-100, kernel_i, kernel_size, C-10) #front
        self.right_properties = Mask(right_path, "Right", alpha/100, beta-100, kernel_i, kernel_size, C-10) #side
        return
    
    def main(self):
        start_time = time.time()
        iteration = 0
        accuracy_arr = {}
        closest = 0
        magn = 100000000

        min_x_goal = 414
        min_y_goal = 75
        max_x_goal = 610
        max_y_goal = 586

        for alpha in range(1, 300, 100): #/100
            for beta in range(0, 200, 100): #-100
                for kernel_size in range(3,7):
                    for kernel_iterations in range(1,5):
                        for C in range(0,20) : #-10   
                            try:
                                iteration += 1
                                self.call(alpha, beta, kernel_size, kernel_iterations, C)
                                #self.common_point()
                                
                                # object_width = self.width()
                                # can_width = 5.93
                                # can_depth = 5.93
                                # accuracy_w = object_width/can_width
                                # print(f"Accuracy: {accuracy_w}%")
                                # object_depth = self.depth()
                                # accuracy_d = object_depth/can_depth
                                
                                # avg = (accuracy_w+accuracy_d)/2
                                min_x = self.min_x()
                                max_x = self.max_x()
                                min_y = self.min_y()
                                max_y = self.max_y()


                                
                                avg_min_x = min_x-min_x_goal
                                avg_max_x = max_x-max_x_goal
                                avg_min_y = min_y-min_y_goal
                                avg_max_y = max_y-max_y_goal

                                avg = (avg_min_x + avg_max_x + avg_min_y + avg_max_y)/4



                                print(f"Average diff for iteration {iteration} is: {avg}")
                                
                                # diff_w = self.positive(accuracy_w-1)
                                # diff_d = self.positive(accuracy_d-1)
                                acc_vector = [avg_min_x,avg_max_x,avg_min_y,avg_max_y]
                                vector_magnitude = math.sqrt(sum(i**2 for i in acc_vector))
                                if vector_magnitude < magn:
                                    magn = vector_magnitude
                                    # final_depth = object_depth
                                    # final_width = object_width
                                    best_index = iteration
                                    #width = self.object_width
                                    #depth = self.object_depth
                                    accuracy_arr = {iteration: avg}
                                    alpha_arr = {iteration: alpha}
                                    beta_arr = {iteration: beta}
                                    kernel_size_arr = {iteration: kernel_size}
                                    kernel_iterations_arr = {iteration: kernel_iterations}
                                    C_arr = {iteration: C}
                            except:
                                #accuracy_arr = {iteration: 0}
                                print(f"Iteration {iteration} failed")
        end_time1 = time.time()
        print(f"Time elapsed 1: {end_time1-start_time}")
        # print(final_depth)
        # print(final_width)
        print(alpha_arr)
        print(beta_arr)
        print(kernel_iterations_arr)
        print(kernel_size_arr)
        print(C_arr)
        

        print(f"Most accurate reading is index: {best_index}, with a diff of {accuracy_arr[best_index]}")





if __name__ == "__main__":
    app = Dimensions()
