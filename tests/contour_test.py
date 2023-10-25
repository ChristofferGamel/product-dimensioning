import unittest
from app.contour import Contoured
import cv2


class TestContourClass(unittest.TestCase):



    def test_angle(self): 


        image_0 = cv2.imread("cam0.jpg")
        image_1 = cv2.imread("cam1.jpg")


        contour = Contoured(image_0)
        point = 719
        fov = 78
        angle = contour.angle(point, fov)
        print(angle)
    


if __name__ == '__main__':
    unittest.main()