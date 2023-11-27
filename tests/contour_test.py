import unittest
from app.contour import Contoured
import cv2
import numpy as np
import random



class TestContourClass(unittest.TestCase):



    def test_angle(self): 
        image_0 = cv2.imread("cam0.jpg")
        contour = Contoured(image_0)
        point = 360
        fov = 78
        angle = contour.angle(point, fov, 720)
        self.assertTrue(angle == 0)

    def test_e2e(self):
        height, width = 300, 400  # You can adjust the size of the image
        image = np.zeros((height, width, 3), dtype=np.uint8)

        left = random.randint(0, width-1)
        right = random.randint(left, width)
        top = random.randint(0, height-1)
        bottom = random.randint(top, height)

        box_color = (255, 255, 255) 
        box_start_point = (left, top)
        box_end_point = (right, bottom)

        cv2.rectangle(image, box_start_point, box_end_point, box_color, thickness=-1)

        contour = Contoured(image)
        contoured = contour.contoured()
        properties = contour.properties()
        print(left == properties["left"], left, properties["left"])
        cv2.imwrite('contoured.jpg',contoured)



if __name__ == '__main__':
    unittest.main()