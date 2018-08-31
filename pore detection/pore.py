import cv2

"""
功能：读取一张图片，显示出来，并转化为HSV色彩空间
"""
image = cv2.imread('./timg.jpg', 1)

# show image
cv2.namedWindow("BGR", 0)
cv2.imshow("BGR", image)

# 中值滤波
img_medianBlur = cv2.medianBlur(image, 5)
font = cv2.FONT_HERSHEY_SIMPLEX
# 均值滤波
img_Blur = cv2.blur(image, (5, 5))
# 高斯滤波
img_GaussianBlur = cv2.GaussianBlur(image, (7, 7), 0)
# 高斯双边滤波
img_bilateralFilter = cv2.bilateralFilter(image, 40, 75, 75)

# show image

# cv2.namedWindow("filter", 0)
# cv2.imshow("filter", img_GaussianBlur)
# cv2.waitKey(0)

# 转化图片到HSV色彩空间
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
H, S, V = cv2.split(hsv)


#  cvResizeWindow("待拼接图像1", 800, 400); //创建一个固定值大小的窗口

# show image
cv2.namedWindow("HSV", 0)
cv2.imshow("HSV", hsv)

# cv2.namedWindow("S", 0)
# cv2.imshow("S", S)
# cv2.waitKey(0)


# threshold ,otsu method
threshold, imgOtsu_S = cv2.threshold(
    S, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# cv2.namedWindow("otsu_S", 0)
# cv2.imshow("otsu_S", imgOtsu_S)
# cv2.waitKey(0)

#
threshold, imgOtsu_V = cv2.threshold(
    V, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# cv2.namedWindow("otsu_V", 0)
# cv2.imshow("otsu_V", imgOtsu_V)
# cv2.waitKey(0)

masked = cv2.bitwise_and(imgOtsu_S, imgOtsu_V)

# cv2.namedWindow("masked", 0)
# cv2.imshow("masked", masked)
# cv2.waitKey(0)

# 定义结构元素
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 闭运算
# closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
# 显示腐蚀后的图像
# cv2.imshow("Close",closed);

# 开运算
opened = cv2.morphologyEx(masked, cv2.MORPH_OPEN, kernel)
# 显示腐蚀后的图像
cv2.namedWindow("open", 0)
cv2.imshow("open", opened)
cv2.waitKey(0)

cv2.destroyAllWindows()
