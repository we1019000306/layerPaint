import math

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import xlrd
import re
import os
from mpl_toolkits.axisartist import axis_artist
import mpl_toolkits.axisartist as axisartist
from brokenaxes import brokenaxes
import cv2
import gc,psutil
import objgraph

figArray = []

def drawPlotWithParameter():
    picWidth = 1920
    picHeight = 1080
    picDPI = 200

    locDict = getDataFromExcel()
    xPointArray = locDict['x']
    yPointArray = locDict['y']
    #y1PointArray = locDict['y1']
    titleX = xPointArray[0]
    titleY = yPointArray[0]
    del xPointArray[0]
    del yPointArray[0]

    fig = plt.figure(figsize=(picWidth/picDPI, picHeight/picDPI), dpi=picDPI)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    x = np.array(xPointArray)
    y = np.array(yPointArray)
    #ax = axisartist.Subplot(fig, 111)
    #fig.add_axes(ax)
    plt.subplot(1,1,1)


    maxX = max(xPointArray)
    minX = min(xPointArray)
    maxY = max(yPointArray)
    minY = min(yPointArray)

    #plt.xticks(np.linspace(minX,maxX,13))
    plt.xticks(np.arange(0,(maxX + caculateUnitStep(maxX,minX)),step = caculateUnitStep(maxX,minX)))
    #plt.yticks(np.linspace(0,maxY,yUnitNum))
    plt.yticks(np.arange(0, (maxY + caculateUnitStep(maxY,minY)), step = caculateUnitStep(maxY,minY)))
    plt.xticks(rotation = '90')
    plt.yticks(rotation='90')
    # if unit2 == '':
    #     plt.title(title + "/\n" + "$(%s)$" % (unit1))
    # elif unitNum == 1:
    #     plt.title(title + "/\n" + "$(%s*%s$)" % (unit1, unit2))
    # else:
    #     plt.title(title + "/\n" + "$(%s*%s^{%d})$" % (unit1, unit2, unitNum))
    #plt.title(handleTitleUnit(title))
    #plt.xlabel(xlabel=(handleTitleUnit(titleX)),fontdict=dict(fontsize=10, color='r',family='SimHei', weight='light', style='italic',))
    plt.ylabel(ylabel=(handleTitleUnit(titleY)),fontdict=dict(fontsize=10, color='r',family='SimHei', weight='light', style='italic',))
    #plt.title(handleTitleUnit(titleX),fontdict=dict(fontsize=10, color='r',family='SimHei', weight='light', style='italic',))
    plt.xlabel(xlabel=(handleTitleUnit(titleX)),fontdict=dict(fontsize=10, color='r',family='SimHei', weight='light', style='italic',),rotation=90)

    ax = plt.gca()
    ax.set_ylim(0)
    ax.set_xlim(0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['left'].set_position(('data', 0))
    # ax.spines['top'].set_position(('data', 0))
   # ax.xaxis.set_ticks_position('top')  # 将x轴的位置设置在顶部
    #ax.yaxis.set_ticks_position('left')  # 将y轴的位置设置在右左边

    # 通过set_visible方法设置绘图区所有坐标轴隐藏
    #ax.axis[:].set_visible(False)
    #ax.invert_yaxis()  # y轴反向
    # ax.new_floating_axis代表添加新的坐标轴
    #ax.axis["x"] = ax.new_floating_axis(0, 0)
    # 给x坐标轴加上箭头
   # ax.axis["x"].set_axisline_style("-|>", size=1.0)
    # 添加y坐标轴，且加上箭头
    #ax.axis["y"] = ax.new_floating_axis(1, 0)
   # ax.axis["y"].set_axisline_style("-|>", size=1.0)

    # 设置x、y轴上刻度显示方向
   # ax.axis["x"].set_axis_direction("top")
    #ax.axis["y"].set_axis_direction("left")

   # ax.axis['y'].set_
    #ax.axis["x"] = ax.new_floating_axis(0, 0)
    # 给x坐标轴加上箭头
   # ax.axis["x"].set_axisline_style("->", size=1.0)

    #plt.xticks(rotation=45)
    #ax.invert_yaxis()
    plt.plot(x, y, color='r', linewidth=1, linestyle='solid')#dotted
    #plt.suptitle("RUNOOB subplot Test")
    plt.savefig(os.getcwd()+'\\'+'1.png',bbox_inches='tight')

    plt.show()

#------------------------旋转图片-------------------------------------
def rotatePic():
    # 读取图片
    src = cv2.imread(os.getcwd() + '\\' + '1.png', cv2.IMWRITE_EXR_COMPRESSION_ZIP)

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

#------------------------从Excel中读取数据-------------------------------------

def getDataFromExcel():
    try:
        wb = xlrd.open_workbook(r'D:/pycharm/layerPaint/test.xlsx')
        yPointArray = wb.sheet_by_name('Sheet1').col_values(0)
        #del yPointArray[0]
        picTotalNum = len(wb.sheets())
    except IndexError:
        print('当前数据缺失')
    else:
        print('数据写入成功')
        pass

    try:
        xPointArray = wb.sheet_by_name('Sheet1').col_values(0)
        yPointArray = wb.sheet_by_name('Sheet1').col_values(1)
        y1PointArray = wb.sheet_by_name('Sheet1').col_values(2)
        locationDict = {'x':xPointArray,'y':yPointArray,'y1':y1PointArray}
        return locationDict

    except IndexError:
        print('当前数据缺失')
    else:
        print('数据写入成功')
        pass
#------------------------utils-----------------------------------------------
#------------------------计算等差数列的公差-------------------------------------
def caculateUnitStep(maxNum:int,minNum:int)->int:
    # maxNum = int(maxNum)
    # minNum = int(minNum)
    if (maxNum / 1000) % 10 > 1:
        return math.trunc((maxNum / 1000) % 10)*100
    else:
        if (maxNum / 100) % 10 > 1:
            return 50
        else:
            if (maxNum / 10) % 10 > 1:
                if 0 <=maxNum - minNum <10:
                    if 0 <= maxNum <10:
                        return 1
                    elif 10 <=maxNum <20:
                        return 2
                    elif 20 <=maxNum <30:
                        return 5
                    elif 30 <=maxNum <50:
                        return 10
                    elif 50 <=maxNum <100:
                        return 20
                    elif 100 <=maxNum <1000:
                        return 100
                    else:
                        return 10
                elif 10 <= maxNum - minNum <20:
                    return 2
                elif 20 <= maxNum - minNum <30:
                    return 15
                elif 30 <= maxNum - minNum <40:
                    return 10
                elif 40 <= maxNum - minNum < 50:
                    return 10
                elif 50 <= maxNum - minNum < 60:
                    return 10
                elif 60 <= maxNum - minNum < 70:
                    return 20
                elif 70 <= maxNum - minNum < 80:
                    return 20
                elif 80 <= maxNum - minNum < 90:
                    return 20
                elif 90 <= maxNum - minNum < 100:
                    return 10
                elif 100 <= maxNum - minNum < 500:
                    return 10
                elif 500 <= maxNum - minNum < 1000:
                    return 10
            else:
                return 1
#----------------------------------------------------------------------------

#------------------------------处理单位上下标----------------------------------
def handleTitleUnit(title):
    # re.findall('\+\d', title, re.M | re.I)
    # re.findall('\-\d', title)
    # print(re.findall('\+\d', title, re.M | re.I))
    # print(re.findall('\-\d', title)[0])
    try:
        if re.findall('\d+', title):
            if re.findall('\-\d+', title):
                title = title.replace(re.findall('\-\d+', title)[0], ('$^{%-d}$') % int(re.findall('\-\d+', title)[0]))
                return title
            elif re.findall('\d+', title):
                title = title.replace(re.findall('\d+', title)[0], ('$^{%d}$') % int(re.findall('\d+', title)[0]))
                return title
            else:
                return title
        else:
            return title
    except IndexError:
        return title

    else:
        return title


def show_memory_info(hint):
    # 获取当前进程的进程号
    pid = os.getpid()

    # psutil 是一个获取系统信息的库
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss/1024./1024
    print(f"{hint} memory used: {memory} MB ")

# $(% s * % s ^ {% d})$
def func():
    a = [1, 2, 3]
    b = [4, 5, 6]

    a.append(b)
    b.append(a)

    objgraph.show_refs([a])

if __name__ == '__main__':
   #  x = [1321,213,15,156,123,1561,15,15,10,0,1,2200]
   #  y = [10,20,33,41,20,12,35,14,12,356,31,4]
   # # drawPlotWithParameter(np.linspace(0,2500,12),np.random.randint(13,size = 12),'hahaha','g','cm',-1,'b')
   #  drawPlotWithParameter()
   #  rotatePic()
    #a,b,c,d = 1,1,1,3
    # print(id(a))
    # print(id(b))
    # print(id(c))
    func()


    #handleTitleUnit(r'转盘转速/r*min100')
    # print(math.trunc((2410 / 1000) % 10)*100)
    # print((2410 / 1000) % 10 > 1)

    pass
