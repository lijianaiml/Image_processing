# encoding: utf-8

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import measure
# from matplotlib.font_manager import *
import json
import time
from logutils import logger


def detect(image_path, imageT_path):
  """

  """

  try:
    # start_time = time.time()
    image_save_path = image_path
    # image_path = image_path + '/1.jpg'
    # imageT_path = imageT_path + '/tshape_face.jpg'
    image_path = image_path + '/1.jpg'
    imageT_path = imageT_path + '/tshape_face.jpg'
    image = cv2.imread(image_path)
    imageT = cv2.imread(imageT_path)
    # 构造返回dic
    dic_cord = {"result": False, "cords": [], "size_avg": 0.0, "except": None}

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换了灰度化
    imageT = cv2.cvtColor(imageT, cv2.COLOR_BGR2GRAY)
    # =================================================================
    # 阈值分割：使用高斯核阈值分割，并通过大津法的分割结果去除边缘噪声
    # =================================================================

    # T区切割
    resT, T = cv2.threshold(imageT, 245, 255, cv2.THRESH_BINARY)
    imageT_gray = image_gray & T

    # cv2.namedWindow('t', 0)
    # cv2.imshow('t', T)
    # cv2.waitKey(0)

    # 自适应阈值分割(gauss)
    image_gauss = cv2.adaptiveThreshold(
        imageT_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 17, 6)

    # OTSU阈值分割
    threshold, image_otsu = cv2.threshold(
        imageT_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

   # 去除阈值分割边缘信息
    image_seg_noborder = image_otsu & image_gauss

    # 可视化
    titles = ['image_gray', 'T', 'imageT_gray',
              'image_gauss', 'image_otsu', 'image_seg_noborder']
    images = [image_gray, T, imageT_gray,
              image_gauss, image_otsu, image_seg_noborder]
    # 使用Matplotlib显示
    for i in range(6):
      plt.subplot(2, 3, i + 1)
      plt.imshow(images[i], 'gray')
      plt.title(titles[i], fontsize=8)
      plt.xticks([]), plt.yticks([])  # 隐藏坐标轴
    plt.show()

    cv2.namedWindow('image_gauss', 0)
    cv2.imshow('image_gauss', image_gauss)
    cv2.waitKey(0)

    cv2.namedWindow('image_otsu', 0)
    cv2.imshow('image_otsu', image_otsu)
    cv2.waitKey(0)

    cv2.namedWindow('image_seg_noborder', 0)
    cv2.imshow('image_seg_noborder', image_seg_noborder)
    cv2.waitKey(0)

    # =================================================================
    # 连通域分析：满足毛孔特征的必要条件 1.毛孔像素8连通 2.毛孔像素区间[4,30]
    # 3.正方形 4.离心率 自适应
    # =================================================================
    # 连通域分析
    # connectivity 1:4连通域标记 2:8连通域标记
    labels = measure.label(image_seg_noborder, connectivity=2)
    props = measure.regionprops(labels)
    props_after = []  # 经过筛选后的连通域属性列表
    eccentricity_after = []  # 经过筛选后的属性的离心率列表
    cords = []  # 连通域坐标列表(row, col)
    sizes = []  # 连通域大小列表

# 根据大小[4,30] 以及 正方形筛选连通域
    for prop in props:
      min_row, min_col, max_row, max_col = prop.bbox
      area = prop.area
      eccentricity = prop.eccentricity
      if 4 <= area <= 30 and (max_row - min_row) == (max_col - min_col):
        props_after.append(prop)
        eccentricity_after.append(eccentricity)

# 计算自适应离心率
    eccentricity_adaptive = np.mean(np.array(eccentricity_after))

# 根据自适应离心率筛选最终毛孔
    for prop_after in props_after:
      if prop_after.eccentricity <= eccentricity_adaptive:
        cords.append(prop_after.centroid)
        sizes.append(prop_after.area)

    pore_size = 0.0
    if len(sizes) > 0:
      pore_num = len(cords)
      pore_size = np.mean(np.asmatrix(sizes))

  # 构造坐标json
    dic_cord["result"] = True
    dic_cord["cords"] = cords
    dic_cord["size_avg"] = pore_size
    dic_json = json.dumps(dic_cord)

    # #最终的成果图
    binary, contours, hierarchy = cv2.findContours(
        T, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (255, 54, 99), 2)
    for (y, x) in cords:
      cv2.circle(image, (int(x), int(y)), 7, (255, 54, 99), 2)

    # 保存生成图片
    cv2.imwrite(image_save_path + '/11.jpg', image)

    # cv2.namedWindow('re', 0)
    # cv2.imshow('re', image)
    # cv2.waitKey(0)

    # cost_time = time.time() - start_time
    # print(cost_time)
    return dic_json

  except Exception as e:

    logger.debug("毛孔检测服务错误：" + str(e))
    dic_cord["result"] = False
    dic_cord["except"] = e.args
    dic_json = json.dumps(dic_cord)
    return dic_json
  finally:
    pass


if __name__ == '__main__':
  # test
  image = cv2.imread('./data/bear.jpg')
  imageT = cv2.imread('./data/bear_tshape.jpg')
  detect('./data', './data')
  # release
  # detect(sys.argv[1],sys.argv[2])
