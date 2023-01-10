import os

import cv2
import numpy as np

# 读取图片
src = cv2.imread(os.getcwd() + '\\' + '1.png', cv2.IMREAD_UNCHANGED)

# 原图的高、宽 以及通道数
rows, cols, channel = src.shape

# 绕图像的中心旋转
# 参数：旋转中心 旋转度数 scale
M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 270, 0.5)
# 参数：原始图像 旋转参数 元素图像宽高
rotated = cv2.warpAffine(src, M, (cols, rows))

# 显示图像
cv2.imshow("src", src)
cv2.imshow("rotated", rotated)
cv2.waitKey(0)
