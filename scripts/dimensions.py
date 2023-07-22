import cv2
import numpy as np

class Mask():
    def __init__(self) -> None:
        image_path = "./pictures/cola.jpg"
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
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        
        con = self.image.copy() 
        cv2.drawContours(con, contours, -1, (0, 255, 0), 3)
        
        largest_contour = max(contours, key=cv2.contourArea)
        image_with_polygon = self.image.copy() 
        cv2.drawContours(image_with_polygon, [largest_contour], 0, (0, 255, 0), thickness=2)
        
        return con

    def contour2(self, image):
        # convert the image to grayscale format
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # apply binary thresholding
        ret, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
                                            
        # draw contours on the original image
        image_copy = self.image.copy()
        cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)

        # for i in range(len(contours)):
        #     for j in range(i+1, len(contours)):
        #         # Calculate the centroids of the contours
        #         centroid_i = np.mean(contours[i], axis=0).astype(np.int32)
        #         centroid_j = np.mean(contours[j], axis=0).astype(np.int32)

        #         # Draw a line between the centroids
        #         cv2.line(image, tuple(centroid_i[0]), tuple(centroid_j[0]), (0, 255, 0), 2)

        for contour in contours:
            # Approximate the contour with a polygon
            epsilon = 0.14 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Draw the polygon
            cv2.polylines(image, [approx], True, (0, 255, 0), 2)

                        
        return image_copy

    def polygon(self, image):
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        print("contours", contours[1])
        largest_contour = contours[1]#max(contours[1], key=cv2.contourArea)
        print("largest: ", largest_contour)
        
        #approx poly curve
        epsilon = 0.01 * cv2.arcLength(largest_contour, True)
        print("epsilon ", epsilon)
        polygon = cv2.approxPolyDP(largest_contour, epsilon, True)
        print("poly ",polygon)
        
        #mask
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [polygon], 0, 255, thickness=cv2.FILLED)
        
        # Apply the mask to the image
        masked_image = cv2.bitwise_and(image, image, mask=mask)
        
        #draw
        image_with_polygon = masked_image.copy()
        cv2.drawContours(image_with_polygon, [polygon], 0, (0, 0, 255), thickness=2)
        
        return image_with_polygon


    def show(self):
        cv2.imshow("original", self.image)
        contrasted = self.contrast(self.image, 0.8110236220472441, 100)
        cv2.imshow("contrasted", contrasted)
        thresholded = self.thresholding(contrasted)
        cv2.imshow("thresholded", thresholded)
        eroded = self.erosion(thresholded)
        print("contouring")
        contoured = self.contour(eroded)
        print("contoured")
        cv2.imshow("contoured", contoured)
        print("showed")
        polygoned = self.polygon(eroded)

        
        cv2.imshow("polygoned", polygoned)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def nothing(self, x):
        pass

if __name__ == "__main__":
    app = Mask()
