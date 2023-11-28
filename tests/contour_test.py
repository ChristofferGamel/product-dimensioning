import unittest
from app.contour import Contoured
import cv2
import numpy as np
import random
import os

# python -m unittest tests/contour_test.py

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


    def test_e2e(self):
        height, width = 300, 400
        image = np.zeros((height, width, 3), dtype=np.uint8)

        left = random.randint(0, width-1)
        right = random.randint(left, width)
        top = random.randint(0, height-1)
        bottom = random.randint(top, height)

        box_color = (255, 255, 255) 
        box_start_point = (left, top)
        box_end_point = (right, bottom)

        cv2.rectangle(image, box_start_point, box_end_point, box_color, thickness=-1)

        cv2.imwrite('tests/e2e_pictures/org_image.png',image)
        contour = Contoured(image)
        contrasted = contour.contrast(image)
        cv2.imwrite('tests/e2e_pictures/contrasted.png',contrasted)
        removed_bg = contour.remove_bg(contrasted)
        cv2.imwrite('tests/e2e_pictures/removed_bg.png',removed_bg)
        thresholded = contour.thresholding(removed_bg)
        cv2.imwrite('tests/e2e_pictures/thresholded.png',thresholded)
        y1, y2, x1, x2 = contour.extreme_points(thresholded)
        draw = contour.draw_points_box(image, y1, y2, x1, x2)
        cv2.imwrite('tests/e2e_pictures/draw.png',draw)
    
    def test_image_examples(self):
        directory = 'tests/test_pictures'
        index = 0
        for filename in os.listdir(directory):
            print(filename)
            f = os.path.join(directory, filename)
            image = cv2.imread(f)
            contour = Contoured(image)
            contoured = contour.contoured()
            cv2.imwrite(f'tests/contoured_pictures/{index}.png',contoured)
            index += 1

                



if __name__ == '__main__':
    unittest.main()