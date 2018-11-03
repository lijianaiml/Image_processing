import cv2
import numpy as np
import pylab as pl


# 程序一，gaborl滤波器的构建，使用6个尺度分四个方向
# 构建Gabor滤波器


def build_filters():
    filters = []
    ksize = [7, 9, 11, 13, 15, 17]  # gabor尺度，6个
    lamda = np.pi / 2.0  # 波长
    for theta in np.arange(0, np.pi, np.pi / 4):  # gabor方向，0°，45°，90°，135°，共四个
        for K in range(6):
            kern = cv2.getGaborKernel(
                (ksize[K], ksize[K]), 1.0, theta, lamda, 0.5, 0, ktype=cv2.CV_32F)
            kern /= 1.5 * kern.sum()
            filters.append(kern)
    return filters


# 程序二，滤波过程

# Gabor滤波过程
def process(img, filters):
    accum = np.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        np.maximum(accum, fimg, accum)
    return accum


# 程序三，特征图生成并显示

# Gabor特征提取
def getGabor(img, filters):
    res = []  # 滤波结果
    for i in range(len(filters)):
        res1 = process(img, filters[i])
        res.append(np.asarray(res1))

    pl.figure(2)
    for temp in range(len(res)):
        pl.subplot(4, 6, temp + 1)
        pl.imshow(res[temp], cmap='gray')
    pl.show()

    return res  # 返回滤波结果,结果为24幅图，按照gabor角度排列


if __name__ == '__main__':
    filters = build_filters()
    #image = np.array(Image.open('photo.jpg'))
    image = cv2.imread('./wi.jpg', 0)
    getGabor(image, filters)
