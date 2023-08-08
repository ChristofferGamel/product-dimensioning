import cv2
import numpy as np
import math
import time, libcamera
from picamera2 import Picamera2, Preview

class Mask():
    def __init__(self) -> None:
        # Image properties
        

        # Image adjustments:
        self.alpha = 1.45             # contrast
        self.beta = -66.8           # contrast brightness
        self.kernel_size = 3        # erosion
        self.kernel_iterations = 9  # erosion
        self.blocksize = 9         # thresholding
        self.C = 5                  # thresholding
        
        self.cam()
        self.filename = "hand_+_monster.jpg"
        image_path = "test-python.jpg"
        self.image = cv2.imread(image_path)
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]
        self.image = self.ResizeWithAspectRatio(self.image, height=700)


        self.show()
    
    def cam(self):
        picam = Picamera2()
        # picam.create_preview_configuration()
        controls = {"ExposureTime": 1400, 
                    "AnalogueGain": 1.0, 
                    "Brightness": 0,
                    "Sharpness":2,
                    "AwbMode":5
                    }
        config = picam.create_preview_configuration(main={"size": (2304, 1296)}, controls=controls)
        #config2 = picam.set_controls({"ExposureTime": 10000, "AnalogueGain": 1.0})
        picam.configure(config)
        time.sleep(2)

        picam.start()
        time.sleep(2)

        # Capture the image with specific settings
        picam.capture_file("test-python.jpg")

        picam.close()




    def contrast(self, image):
        contrast = cv2.convertScaleAbs(image, alpha=self.alpha, beta=self.beta)
        return contrast
    
    def thresholding(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_8bit = cv2.convertScaleAbs(gray)
        th2 = cv2.adaptiveThreshold(gray_8bit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.blocksize, self.C)
        return th2

    def erosion(self, image):
        kernel = np.ones((self.kernel_size,self.kernel_size),np.uint8)
        er = cv2.erode(image,kernel,iterations = self.kernel_iterations)
        ret, thresh = cv2.threshold(er, 150, 255, cv2.THRESH_BINARY)
        return thresh
    
    def contour(self, image):
        image_with_polygon = self.image.copy()
        contours, hierarchy = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        
        largest_contour = max(contours, key=cv2.contourArea)
        contours_without_largest = [contour for contour in contours if contour is not largest_contour]
        second_largest_contour = max(contours_without_largest, key=cv2.contourArea)
        self.find_extremes(second_largest_contour)        
        cv2.line(image_with_polygon, (self.max_x,self.min_y), (self.max_x,self.max_y), (255, 0, 0), 3)
        cv2.line(image_with_polygon, (self.min_x,self.max_y), (self.max_x,self.max_y), (255, 0, 0), 3)
        cv2.line(image_with_polygon, (self.min_x,self.min_y), (self.min_x,self.max_y), (255, 0, 0), 3)
        cv2.line(image_with_polygon, (self.min_x,self.min_y), (self.max_x,self.min_y), (255, 0, 0), 3)
        cv2.drawContours(image_with_polygon, contours, -1, (0, 255, 0), thickness=2)
        
        for contour in contours:
            # Approximate the contour with a polygon
            epsilon = 0.14 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Draw the polygon
            cv2.polylines(image_with_polygon, [approx], True, (0, 255, 0), 2)
        # cv2.drawContours(image_with_polygon, second_largest_contour, -1, (255, 0, 0), thickness=2)
        
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


    def show(self):
        contrasted = self.contrast(self.image)
        thresholded = self.thresholding(contrasted)
        eroded = self.erosion(thresholded)
        contoured = self.contour(eroded)
        
        print(f"Alpha: {self.alpha}, Beta: {self.beta}, kernel size: {self.kernel_size}, Kernel iterations: {self.kernel_iterations}, C: {self.C}")
        while True:
            cv2.imshow("contrasted", contrasted)
            
            cv2.imshow("thresholded", thresholded)
            
            cv2.imshow("eroded", eroded)
            
            
            cv2.imshow("contoured", contoured)
            cv2.imwrite("contoured_images/"+self.filename, contoured)
            
            key = cv2.waitKey(1) & 0xFF

            
            if key == ord("q"):
                break
        cv2.destroyAllWindows()

    def nothing(self, x):
        pass

if __name__ == "__main__":
    app = Mask()
