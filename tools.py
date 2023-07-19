import cv2
import numpy as np



class Tools():
    def __init__(self) -> None:
        image_path = "cola.jpg"
        self.image = cv2.imread(image_path)
        
        self.contrastTool()

    def contrastTool(self):
        alpha = 2
        beta = 10

        def update_contrast(_):
            nonlocal alpha, beta

            alpha = cv2.getTrackbarPos('alpha', 'Contrast') / 127.0
            beta = cv2.getTrackbarPos('beta', 'Contrast') - 100
            print(alpha, beta)

        cv2.namedWindow("Contrast")
        cv2.createTrackbar('alpha', "Contrast", 0, 127, update_contrast) #[0,127]
        cv2.createTrackbar('beta', "Contrast", 0, 200, update_contrast) #[-100,100]

        while True:
            contrast = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            resize_c = self.ResizeWithAspectRatio(contrast, width=300)

            cv2.imshow("Contrast", resize_c)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()

    def blacken_non_white(self):
        
        
        resize_o = self.ResizeWithAspectRatio(self.image, width=1000)
        

        cv2.imshow("original", resize_o)
        
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Create a mask for pixels within the white range
        mask = cv2.threshold(gray, 105, 255, cv2.THRESH_BINARY_INV)[1]  # #2 = white range

        # Apply the mask to blacken non-white areas
        blackened_image = cv2.bitwise_and(self.image, self.image, mask=mask)

        gray_blackened = cv2.cvtColor(blackened_image, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray_blackened, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        total_area = sum(cv2.contourArea(contour) for contour in contours)

        # cv2.imshow("Blackened Image", blackened_image)
        print("Total area of blackened regions:", total_area)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

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