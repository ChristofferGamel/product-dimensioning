import cv2
import numpy as np

class Mask():
    def __init__(self) -> None:
        image_path = "right.jpg"
        self.image = cv2.imread(image_path)
        self.alpha_v = 1.5
        self.beta_v = 10
        
        #self.blacken_non_white()
        self.contrast()

        alpha = 2
        beta = 10
        w_range = 102

        def update_contrast(_):
            nonlocal alpha, beta, w_range

            alpha = cv2.getTrackbarPos('alpha', 'Contrast')
            beta = cv2.getTrackbarPos('beta', 'Contrast')
            w_range = cv2.getTrackbarPos('w_range', 'Contrast')
            print(alpha, beta, w_range)

        cv2.namedWindow("Contrast")
        cv2.createTrackbar('alpha', "Contrast", 0, 50, update_contrast)
        cv2.createTrackbar('beta', "Contrast", 0, 254, update_contrast)
        cv2.createTrackbar('w_range', "Contrast", 0, 400, update_contrast)

        while True:
            contrast = cv2.convertScaleAbs(self.image, alpha, beta) # 50, 6
            gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

            mask = cv2.threshold(gray, w_range, 255, cv2.THRESH_BINARY_INV)[1]  # #2 = white range

            blackened_image = cv2.bitwise_and(self.image, self.image, mask=mask)

            gray_blackened = cv2.cvtColor(blackened_image, cv2.COLOR_BGR2GRAY)
            _, thresholded = cv2.threshold(gray_blackened, 1, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            total_area = sum(cv2.contourArea(contour) for contour in contours)

            #cv2.imshow("Blackened Image", gray)
            
            resize_c = self.ResizeWithAspectRatio(gray_blackened, width=1000)
            
    
            cv2.imshow("Contrast", resize_c)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


        
    def blacken_non_white(self):
        contrast = cv2.convertScaleAbs(self.image, 33, 122)
        
        resize_o = self.ResizeWithAspectRatio(self.image, width=1000)
        

        cv2.imshow("original", resize_o)
        
        
        gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

        # Create a mask for pixels within the white range
        mask = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)[1]  # #2 = white range

        # Apply the mask to blacken non-white areas
        blackened_image = cv2.bitwise_and(self.image, self.image, mask=mask)

        gray_blackened = cv2.cvtColor(blackened_image, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray_blackened, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total_area = sum(cv2.contourArea(contour) for contour in contours)

        cv2.imshow("Blackened Image", gray)
        print("Total area of blackened regions:", total_area)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def nothing(self, x):
        pass

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
    app = Mask()
