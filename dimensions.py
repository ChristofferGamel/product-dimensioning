import cv2
import numpy as np

class Mask():
    def __init__(self) -> None:
        image_path = "cola.jpg"
        self.image = cv2.imread(image_path)
        self.alpha_v = 0
        self.beta_v = 0
        
        self.show()

    def contrast(self, image, alpha, beta): #0.8110236220472441, 100
        contrast = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return contrast
    

    def thresholding(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_8bit = cv2.convertScaleAbs(gray)
        th2 = cv2.adaptiveThreshold(gray_8bit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
        return th2

    def erosion(self, image):
        kernel = np.ones((1,1),np.uint8)
        er = cv2.erode(image,kernel,iterations = 8)
        return er
    
    def contour(self, image):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        con = cv2.drawContours(image, contours, -1, (0,255,0), 3)
        return con


    def show(self):
        contrasted = self.contrast(self.image, 0.8110236220472441, 100)
        thresholded = self.thresholding(contrasted)
        eroded = self.erosion(thresholded)
        
        
        cv2.imshow("Thresholding", eroded)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def nothing(self, x):
        pass


if __name__ == "__main__":
    app = Mask()