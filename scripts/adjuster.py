import cv2
import numpy as np



class Tools():
    def __init__(self) -> None:
        image_path = "./pictures/cola.jpg"
        self.image = cv2.imread(image_path)
        
        self.contrastTool()

    def contrastTool(self):
        alpha = 2
        beta = 10
        k_size = 1
        k_iterations = 8

        def update_contrast(_):
            nonlocal alpha, beta, k_iterations, k_size

            alpha = cv2.getTrackbarPos('alpha', 'Contrast') / 127.0
            beta = cv2.getTrackbarPos('beta', 'Contrast') - 100
            k_size = cv2.getTrackbarPos('kernel_size', 'Contrast')
            k_iterations = cv2.getTrackbarPos('kernel_iterations', 'Contrast')
            print(f"Alpha: {alpha}, Beta: {beta}, kernel size: {k_size}, Kernel iterations: {k_iterations}")

        cv2.namedWindow("Contrast")
        
        cv2.createTrackbar('alpha', "Contrast", 0, 127, update_contrast) #[0,127]
        cv2.createTrackbar('beta', "Contrast", 0, 200, update_contrast) #[-100,100]
        cv2.createTrackbar('kernel_size', "Contrast", 0, 10, update_contrast) 
        cv2.createTrackbar('kernel_iterations', "Contrast", 0, 10, update_contrast)

        while True:
            contrast = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
            gray_8bit = cv2.convertScaleAbs(gray)
            th2 = cv2.adaptiveThreshold(gray_8bit, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)
            kernel = np.ones((k_size,k_size),np.uint8)
            er = cv2.erode(th2,kernel,iterations = k_iterations)
            
            ret, thresh = cv2.threshold(er, 150, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
                                                
            # draw contours on the original image
            image_copy = self.image.copy()
            cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)

            for contour in contours:
                # Approximate the contour with a polygon
                epsilon = 0.14 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                # Draw the polygon
                cv2.polylines(image_copy, [approx], True, (0, 255, 0), 2)
            resize_c = self.ResizeWithAspectRatio(image_copy, width=300)

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