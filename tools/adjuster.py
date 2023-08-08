import cv2
import numpy as np
from image_processor import Mask



class Tools():
    def __init__(self) -> None:
        image_path = "./captured_images/helmet.jpg"
        self.image = cv2.imread(image_path)
        self.image_height = self.image.shape[0]
        self.image_width = self.image.shape[1]
        self.image = self.ResizeWithAspectRatio(self.image, height=700)
        self.contrastTool()

    def contrastTool(self):
        image_path = "./captured_images/r.jpg"
        alpha = 2
        beta = 10
        k_size = 1
        k_iterations = 8
        blocksize = 11
        C = 4



        def update_contrast(_):
            nonlocal alpha, beta, k_iterations, k_size, C, blocksize

            alpha = cv2.getTrackbarPos('alpha', 'Contrast') / 1000.0
            beta = (cv2.getTrackbarPos('beta', 'Contrast') / 10) -100
            k_size = cv2.getTrackbarPos('kernel_size', 'Contrast')
            k_iterations = cv2.getTrackbarPos('kernel_iterations', 'Contrast')
            blocksize = cv2.getTrackbarPos('blocksize', 'Contrast')
            C = cv2.getTrackbarPos('C', 'Contrast') - 10
            print(f"Alpha: {alpha}, Beta: {beta}, kernel size: {k_size}, Kernel iterations: {k_iterations}, Blocksize: {blocksize} C: {C}")

        cv2.namedWindow("Contrast")
        cv2.createTrackbar('alpha', "Contrast", 0, 3000, update_contrast) 
        cv2.createTrackbar('beta', "Contrast", 0, 2000, update_contrast) #[-100,100]
        cv2.createTrackbar('kernel_size', "Contrast", 0, 10, update_contrast) 
        cv2.createTrackbar('kernel_iterations', "Contrast", 0, 10, update_contrast)
        cv2.createTrackbar('blocksize', "Contrast", 1, 21, update_contrast)
        cv2.createTrackbar('C', "Contrast", 1, 21, update_contrast) #-10

        while True:
            contrasted = self.contrast(self.image, alpha, beta)
            thresh = self.thresholding(contrasted, blocksize, C)
            eroded = self.erosion(thresh, k_iterations, k_size)
            self.image_copy = self.image.copy()
            contoured = self.contour(eroded)
            cv2.imshow("Contrast", contoured)

        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()
    
    def contrast(self, image, alpha, beta):
        ret = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return ret
    
    def thresholding(self, image, blocksize, C):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_8bit = cv2.convertScaleAbs(gray)
        try:
            th2 = cv2.adaptiveThreshold(gray_8bit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, C)
        except:
            print("failed with blocksize: ",blocksize)
            th2 = cv2.adaptiveThreshold(gray_8bit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, C)
        #ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        return th2
    
    def erosion(self, image, kernel_size, kernel_iterations):
        kernel = np.ones((kernel_size,kernel_size),np.uint8)
        er = cv2.erode(image,kernel,iterations = kernel_iterations)
        #ret, thresh = cv2.threshold(er, 150, 255, cv2.THRESH_BINARY)
        return er
    
   
    def find_extremes(self, list):
        self.max_x = 0
        self.max_y = 0
        self.min_y = self.image_height
        self.min_x = self.image_width
        
        
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
    
    
    def contour(self, image):
        contours, hierarchy = cv2.findContours(image=image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        
        try:
            largest_contour = max(contours, key=cv2.contourArea)
            contours_without_largest = [contour for contour in contours if contour is not largest_contour]
            second_largest_contour = max(contours_without_largest, key=cv2.contourArea)
            self.find_extremes(second_largest_contour)
            cv2.line(self.image_copy, (self.max_x,self.min_y), (self.max_x,self.max_y), (255, 0, 0), 3)
            cv2.line(self.image_copy, (self.min_x,self.max_y), (self.max_x,self.max_y), (255, 0, 0), 3)
            cv2.line(self.image_copy, (self.min_x,self.min_y), (self.min_x,self.max_y), (255, 0, 0), 3)
            cv2.line(self.image_copy, (self.min_x,self.min_y), (self.max_x,self.min_y), (255, 0, 0), 3)
            cv2.drawContours(self.image_copy, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)
        except:
            pass
        
        

        for contour in contours:
            # Approximate the contour with a polygon
            epsilon = 0.14 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Draw the polygon
            cv2.polylines(self.image_copy, [approx], True, (0, 255, 0), 2)
        return self.image_copy

        
    
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


if __name__ == "__main__":
    app = Tools()