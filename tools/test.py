import cv2
import numpy as np

src_img = cv2.imread('./captured_images/white.jpg')
average_color_row = np.average(src_img, axis=0)
average_color = np.average(average_color_row, axis=0)
print(average_color)

d_img = np.ones((312,312,3), dtype=np.uint8)
d_img[:,:] = average_color

cv2.imshow('Source image',src_img)
cv2.imshow('Average Color',d_img)
cv2.waitKey(0)