import matplotlib.pyplot as plt
import numpy as np
from docx import Document
import xlrd

ax = plt.subplot()

#-------------------------------------绘图-----------------------------------
def drawPic():
    # plot 1:
    drawPlotWithParameter([0, 12], [0, 2400], 6, 1, True, "机械转速", "m", "h", -1)

    # plot 2:
    drawPlotWithParameter([50, 70], [1, 4], 6, 2, False, "钻压", "kN", "", 0)

    # plot 3:
    drawPlotWithParameter([50,70], [1, 4], 6, 3, False, "转盘转速", "r", "min", -1)

    # plot 4:
    drawPlotWithParameter([20, 40], [1, 4], 6, 4, False, "排量", "L", "s", -1)

    # plot 5:
    drawPlotWithParameter([1, 1.5], [1, 4], 6, 5, False, "钻井液密度", "g", "cm", -3)

    # plot 6:
    drawPlotWithParameter([30, 60],[1, 4],6,6,False,"漏斗粘度","s","",-5)

    plt.suptitle("RUNOOB subplot Test")
    plt.show()

def drawPlotWithParameter(xArray,yArray,picTotalNum,currentNum,leftVisble,title,unit1,unit2,unitNum,color):
    global ax

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    x = np.array(xArray)
    y = np.array(yArray)
    if leftVisble:
        plt.subplot(1, picTotalNum,currentNum,sharey = ax)
    else:
        ax = plt.subplot(1, picTotalNum,currentNum)
    plt.plot(x, y, color=color)
    new_ticks = np.linspace(0,60,3)
    plt.xticks(new_ticks)


    if unit2 == '':
        plt.title(title + "/\n" + "$(%s)$" % (unit1))
    elif unitNum == 1:
        plt.title(title + "/\n" + "$(%s*%s$)" % (unit1, unit2))
    else:
        plt.title(title + "/\n" + "$(%s*%s^{%d})$" % (unit1, unit2, unitNum))

    ax = plt.gca()
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    if leftVisble:
        pass
    else:
        plt.yticks([])
    ax.spines['left'].set_visible(leftVisble)
    ax.xaxis.set_ticks_position('top')  # 将x轴的位置设置在顶部
    ax.yaxis.set_ticks_position('left')  # 将y轴的位置设置在右边
    ax.invert_yaxis()  # y轴反向
    pass

#-----------------------------------数据读写----------------------------------
def getBaseDataFromExcel():
    try:
        wb = xlrd.open_workbook(r'../test.xlsx')
        yPointArray = wb.sheet_by_name('Sheet1').col_values(0)
        del yPointArray[0]
        picTotalNum = len(wb.sheets())
    except IndexError:
        print('当前数据缺失')
    else:
        print('数据写入成功')

    try:
        x1PointArray = wb.sheet_by_name('Sheet1').col_values(1)
        del x1PointArray[0]
        drawPlotWithParameter(x1PointArray,yPointArray,6,1,True,"机械转速", "m", "h", -1,'c')

    except IndexError:
        print('当前数据缺失')
    else:
        print('数据写入成功')

    try:
        x2PointArray = wb.sheet_by_name('Sheet1').col_values(2)
        del x2PointArray[0]
        drawPlotWithParameter(x2PointArray, yPointArray, 6, 2, False, "钻压", "kN", "", 0,'b')
    except IndexError:
        print('当前数据缺失')
    else:
         print('数据写入成功')

    try:
        x3PointArray = wb.sheet_by_name('Sheet1').col_values(3)
        del x3PointArray[0]
        drawPlotWithParameter(x3PointArray, yPointArray, 6, 3, False, "转盘转速", "r", "min", -1,'m')
    except IndexError:
        print('当前数据缺失')
    else:
        print('数据写入成功')

    try:
        x4PointArray = wb.sheet_by_name('Sheet1').col_values(4)
        del x4PointArray[0]
        drawPlotWithParameter(x4PointArray, yPointArray, 6, 4, False, "排量", "L", "s", -1,'k')
    except IndexError:
        print('当前数据缺失')
    else:
        print('数据写入成功')

    try:
        x5PointArray = wb.sheet_by_name('Sheet1').col_values(5)
        del x5PointArray[0]
        drawPlotWithParameter(x5PointArray, yPointArray, 6, 5, False, "钻井液密度", "r", "cm", -3,'r')
    except IndexError:
        print('当前数据缺失')
    else:
        print('数据写入成功')

    try:
        x6PointArray = wb.sheet_by_name('Sheet1').col_values(6)
        del x6PointArray[0]
        drawPlotWithParameter(x6PointArray, yPointArray, 6, 6, False, "漏斗粘度", "g", "", -1,'g')
    except IndexError:
        print('当前数据缺失')
    else:
        print('数据写入成功')

    plt.suptitle("RUNOOB subplot Test")
    plt.show()

if __name__ == '__main__':
    #drawPic()
    getBaseDataFromExcel()

    pass


