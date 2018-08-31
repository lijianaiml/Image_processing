import cv2
import numpy as np

bgr = cv2.imread('./blue-sky.jpg', 1)


hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)


# HSV中blue范围
lower_blue = np.array([78, 43, 46])
upper_blue = np.array([120, 255, 255])

# 获得blue区域的mask
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 和原始图片进行and操作，获得blue区域
res = cv2.bitwise_and(bgr, bgr, mask=mask)

cv2.namedWindow("bgr", 0)
cv2.imshow("bgr", bgr)
cv2.namedWindow("hsv", 0)
cv2.imshow("hsv", hsv)
cv2.namedWindow("mask", 0)
cv2.imshow("mask", mask)
cv2.namedWindow("res", 0)
cv2.imshow("res", res)

cv2.waitKey(0)

cv2.destroyAllWindows()
