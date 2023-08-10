import cv2
import numpy as np
import math
import time
import time, libcamera
from picamera2 import Picamera2, Preview
from rembg import remove


class Mask():
    def __init__(self) -> None:
        # Image properties
        

        # Image adjustments:
        self.alpha = 1.2             # contrast
        self.beta = 50           # contrast brightness
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
        controls = {"ExposureTime": 1600, 
                    "AnalogueGain": 1.2, 
                    "Brightness": 0.08,
                    "Sharpness":3,
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
    
    def remove_bg(self, image):
        removed_bg = remove(image)
        return removed_bg
    
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
        y1, y2, x1, x2 = self.extreme_points(eroded)
        draw = self.draw_points_box(self.image, y1, y2, x1, x2)

        #contoured = self.contour(eroded)
        unique_value = time.time()
        orig = f"OR_{unique_value}.jpg"
        cont = f"CO_{unique_value}.jpg"
        cv2.imwrite("tools/stress_test_run/"+orig, self.image)
        cv2.imwrite("tools/stress_test_run/"+cont, draw)
        print(f"File names: {orig}, {cont}")
        
        
        
        print(f"Alpha: {self.alpha}, Beta: {self.beta}, kernel size: {self.kernel_size}, Kernel iterations: {self.kernel_iterations}, C: {self.C}")
        while True:
            cv2.imshow("1", contrasted)
            cv2.imshow("c", thresholded)
            cv2.imshow("contoured", draw)
            
            
            key = cv2.waitKey(1) & 0xFF

            
            if key == ord("q"):
                break
        cv2.destroyAllWindows()

    def nothing(self, x):
        pass

if __name__ == "__main__":
    app = Mask()
