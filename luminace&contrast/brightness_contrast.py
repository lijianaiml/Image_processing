import cv2
import numpy as np

# 回调函数，根据亮度及对比度值作处理


def ContrastAndBright(x=0):
  bright = cv2.getTrackbarPos('bright', 'image')
  contrast = cv2.getTrackbarPos('contrast', 'image')
  res = np.uint8(np.clip((contrast * origin + bright), 0, 255))
  tmp = np.hstack((origin, res))  # 两张图片横向合并（便于对比显示）
  cv2.imshow("image", tmp)


origin = cv2.imread('./l&c.jpg', 1)

bright = 0
contrast = 1
cv2.namedWindow('image', 0)

# create trackbars for color change
cv2.createTrackbar('bright', 'image', bright, 255, ContrastAndBright)
cv2.createTrackbar('contrast', 'image', contrast, 10, ContrastAndBright)

ContrastAndBright()

cv2.waitKey(0)
cv2.destroyAllWindows()
