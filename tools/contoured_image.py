import cv2
import numpy as np
from matplotlib import pyplot as plt
from rembg import remove
from contour import Contoured


class Mask():
    def __init__(self) -> None:
        image_path = "./tools/monster.jpg"
        image = cv2.imread(image_path)
        self.show(image)

    

    def show(self, image):
        class_init = Contoured()
        contoured = class_init.main(image)
        
        while True:
            cv2.imshow("Contoured", contoured)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        cv2.destroyAllWindows()
        
        
if __name__ == "__main__":
    app = Mask()
