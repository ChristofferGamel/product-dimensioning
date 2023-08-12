import cv2
import numpy as np
import math
import time
import time, libcamera
from picamera2 import Picamera2, Preview
from rembg import remove


class Mask():
    def __init__(self) -> None:
        # Image adjustments:
        self.alpha = 1.45          # contrast
        self.beta = -100           # contrast brightness
        self.blocksize = 9         # thresholding
        self.C = 5                 # thresholding
        
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
        picam.configure(config)
        
        time.sleep(2)
        picam.start()
        time.sleep(2)

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
        # Processing
        contrasted = self.contrast(self.image)
        removed = self.remove_bg(contrasted)
        thresholded = self.thresholding(removed)
        y1, y2, x1, x2 = self.extreme_points(thresholded)
        draw = self.draw_points_box(self.image, y1, y2, x1, x2)

        # File saving
        unique_value = time.time()
        orig = f"OR_{unique_value}.jpg"
        cont = f"CO_{unique_value}.jpg"
        cv2.imwrite("tools/stress_test_run/"+orig, self.image)
        cv2.imwrite("tools/stress_test_run/"+cont, draw)
        print(f"File names: {orig}, {cont}")
        
        while True:
            # cv2.imshow("1", contrasted)
            # cv2.imshow("removed", removed)
            # cv2.imshow("c", thresholded)
            
            cv2.imshow("contoured", draw)
            
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = Mask()
