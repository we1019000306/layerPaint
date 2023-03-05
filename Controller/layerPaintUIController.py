# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layerPaintUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidgetItem, QColorDialog, QMessageBox, QDialog, QLabel, \
    QHeaderView
from PyQt5.Qt import QThread,QMutex,pyqtSignal
import time
from PyQt5 import QtCore, QtWidgets,QtGui


from LMYUntils.myStringUtil import getImgUrl
from View.layerPaintUI import Ui_MainWindow
import sys
import pandas as pd
from LMYUntils import myStringUtil,myArangeUtil
import matplotlib.pyplot as plt
import numpy as np
import os
from Controller.previewDialogController import previewDialog
from Controller import previewDialogController

dataDictList:list = []
dataDictKey:list = []
figList:list = []
newYDataList:list = []
xDataList:list = []
tableHeaderList:list = []
pd.set_option('display.max_columns', None)   #显示完整的列
pd.set_option('display.max_rows', None)  #显示完整的行
class window(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        global newYDataList
        global xDataList
        super().__init__()
        self.setupUi(self)
        self.y1LineColorPushButton.clicked.connect(self.lineColorPushButtonClicked)
        self.selectFileButton.clicked.connect(self.getFileOnClicked)
        self.selectFileButton.clicked.connect(self.loadBaseData)
        self.previewPushButton.clicked.connect(self.previewButtonClicked)
        self.savePushButton.clicked.connect(self.savePushButtonClicked)
        self.xComboBox.activated[str].connect(self.XComboBoxValueChanged)
        self.y1ComboBox.activated[str].connect(self.YComboBoxValueChanged)
        self.addYpushButton.clicked.connect(self.addYDataButtonClicked)
        self.deleteYPushButton.clicked.connect(self.deleteYDataButtonClicked)
        self.y1LineColorPushButton.setText('#000000')
        self.y1LineColorPushButton.setStyleSheet('QWidget {background-color:#000000}')
        self.y1LineWidthDoubleSpinBox.setValue(1.0)

        xDataList.append([self.xLabel,
                             self.xComboBox,
                             self.xTitleTextEdit,
                             self.xMaxXLineEdit,
                             self.xMinXLineEdit,
                             self.xStepLineEdit,
                             self.widthLineEdit,
                             self.heightLineEdit,
                             self.dpitLineEdit,
                             self.pictureNameLineEdit])
        newYDataList.append([self.y1Label,
                             self.y1ComboBox,
                             self.y1TitleTextEdit,
                             self.y1LineTypeComboBox,
                             self.y1LineWidthDoubleSpinBox,
                             self.y1LineColorPushButton,
                             self.y1MaxYLineEdit,
                             self.y1MinYLineEdit,
                             self.y1StepLineEdit])

        # self.mainGridLayout.setContentsMargins(6, 10, 6, 10)

        # np数组生成的图
        #len_x = show_image.shape[1]  # 获取图像大小
        #wid_y = show_image.shape[0]
        #frame = QImage(show_image.data, len_x, wid_y, len_x * 3, QImage.Format_RGB888)  # 此处如果不加len_x*3，就会发生倾斜
        #pix = QPixmap.fromImage(frame)

    def getFileOnClicked(self):
        self.selectFileButton.setEnabled(False)
        self.thread_2 = Thread_2()
        self.thread_2._signal.connect(self.setSelectFileButtonEnable)
        self.thread_2.start()
        fileName, fileType = QFileDialog.getOpenFileName(self,
                                                         "打开表格",
                                                         "",
                                                         "*.xlsx;*.xls;;All Files(*)")
        global path_openfile_name

        ###获取路径====================================================================
        if fileName == '':
            print('111111')
            path_openfile_name = ''
            pass
        else:
            path_openfile_name = fileName

    def loadBaseData(self):
        global dataDictKey
        global path_openfile_name
        global dataDictList
        global newYDataList
        global tableHeaderList
        dataDictList.clear()
        dataDictKey.clear()
        tableHeaderList.clear()

        # self.XComboBox.addItem('x轴')
        # self.y1ComboBox.addItem('y轴')
        ###===========读取表格，转换表格，===========================================
        if  path_openfile_name != '':
            input_table = pd.read_excel(path_openfile_name)
            # print(input_table)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]
            dataDictKey = input_table.columns.values.tolist()
            print(dataDictKey)
            #表头
            input_table_header = input_table.columns.values.tolist()


            ###===========读取表格，转换表格，============================================

            ###======================给tablewidget设置行列表头============================
            self.dataTableWidget.setColumnCount(input_table_colunms)
            self.dataTableWidget.setRowCount(input_table_rows)
            self.dataTableWidget.setHorizontalHeaderLabels(input_table_header)
            self.dataTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.dataTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            ###================遍历表格每个元素，同时添加到tablewidget中========================
            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
               # print(input_table_rows_values)
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                #print(input_table_rows_values_list)
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    ###==============将遍历的元素添加到tablewidget中并显示=======================

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(4 | 128)
                    self.dataTableWidget.setItem(i, j, newItem)

                    ###================遍历表格每个元素，同时添加到tablewidget中========================

                    # 刷新界面命令：
            #self.XComboBox.addItems(['1', '2', '3'])
            tableHeaderList = myStringUtil.deleteBlankStringWithList(input_table_header)
            # if 0 < len(dataDictKey):
            self.getDataFromTableWidget()
            if len(newYDataList) > 0 and len(dataDictList) > 0:
                # self.XComboBox.addItem('x轴')
                xDataList[0][1].clear()
                xDataList[0][1].addItems(tableHeaderList)
                xDataList[0][1].setCurrentIndex(0)
                self.adaptXEdit()
                self.adaptXTitle()
                for i in newYDataList:
                    i[1].clear()
                    i[1].addItems(tableHeaderList)
                    i[2].setPlainText(i[1].currentText())
                    i[3].setCurrentIndex(0)
                    i[4].setValue(1.0)
                    if i[5].text() == '连线颜色':
                        i[5].setText('#000000')
                        i[5].setStyleSheet('QWidget {background-color:#000000}')
                    yArray = dataDictList[i[1].currentIndex()]
                    yFloatArray = []
                    for m in yArray:
                        yFloatArray.append(float(m))
                    yMax = float(max(yFloatArray))
                    yMin = float(min(yFloatArray))
                    yStep = myArangeUtil.caculateUnitStep(yMax, yMin)
                    i[6].setText(str(yMax))
                    i[7].setText(str(yMin))
                    i[8].setText(str(yStep))
                # print(dataDictList[self.XComboBox.currentIndex()])
                # print(dataDictList[self.y1ComboBox.currentIndex()])
                # print(self.y1LineColorPushButton.text())
                # if self.y1LineColorPushButton.text() == '连线颜色':
                #     self.y1LineColorPushButton.setText('#000000')
                #     self.y1LineColorPushButton.setStyleSheet('QWidget {background-color:#000000}')
                #
                # print(self.XComboBox.currentIndex())
                # # 处理当未选择X轴或Y轴时默认的预览图
                # xDictList = [self.XComboBox.currentText()]
                # yDictList = [self.y1ComboBox.currentText()]
                # for i in dataDictKey:
                #     xDictList.append(i)
                #     yDictList.append(i)
            # self.XComboBox.adjustSize()
            # self.y1ComboBox.adjustSize()

            #图片名称
            #self.pictureNameLineEdit.setText()
            QApplication.processEvents()


        else:
            if len(dataDictKey) > 0:
                QMessageBox.information(MainWindow,
                                        '提示！！', '你已取消更新数据源！！')
            else:
                QMessageBox.information(MainWindow,
                                        '提示！！', '你已取消导入数据源！！')




        # qApp = QApplication.instance()
        # qApp.quit()

    # def eventFilter(self, obj, event):
    #
    #     AllItems = [self.combo.itemText(i) for i in range(self.combo.count())]
    #     if obj == self.combo:
    #         if event.type() == QEvent.FocusOut:
    #             if self.combo.lineEdit().text() not in AllItems and self.combo.lineEdit().text() != '':
    #                 self.combo.addItems(self.combo.lineEdit().text());
    #     return QWidget.eventFilter(self, obj, event)

    def lineColorPushButtonClicked(self):
        self.thread_5 = Thread_5()
        self.thread_5.start()
        self.showDialog()
        pass

    def previewButtonClicked(self):
       global dataDictList
       global dataDictKey

       self.thread_3 = Thread_3()
       self.thread_3._reloadUISignal.connect(self.setPreviewButtonEnable)
       self.thread_3.start()
       self.getDataFromTableWidget()
       if(len(dataDictList)>0):
           screenDesktop = QApplication.desktop()
           screenRect = screenDesktop.screenGeometry()
           screenHeight = int(screenRect.height())
           screenWidth = int(screenRect.width())

           if self.widthLineEdit.text() == '' or self.heightLineEdit.text() =='' or self.dpitLineEdit.text() =='':
               QMessageBox.information(self.previewPushButton,
                                       '警告!!!', '宽度、高度和dpi不能为空值!!!')
           elif not (myStringUtil.isNumber(self.widthLineEdit.text())
                   and myStringUtil.isNumber(self.heightLineEdit.text())
                   and myStringUtil.isNumber(self.dpitLineEdit.text())):
               QMessageBox.information(self.previewPushButton,
                                       '警告!!!','请输入数字！！')
           elif int(self.widthLineEdit.text()) > screenWidth +1000:
               QMessageBox.information(self.previewPushButton,
                                       '警告!!!',
                                       ('图片宽度不可以大于屏幕宽度！！！\n提示当前屏幕为%d*%d！！！')%(screenWidth,screenHeight))
           elif int(self.heightLineEdit.text()) > screenHeight+1000:
               QMessageBox.information(self.previewPushButton,
                                       '警告!!!',
                                       ('图片宽度不可以大于屏幕高度！！！\n提示当前屏幕为%d*%d！！！')%(screenWidth,screenHeight))
           elif int(self.dpitLineEdit.text()) <10:
               QMessageBox.information(self.previewPushButton,
                                       '警告!!!','dpi至少大于10!!!')
           else:
               print(dataDictList)
               xNoNoneArray,yNoNoneArray = handlerUnlegalData(dataDictList[xDataList[0][1].currentIndex()],
                                  dataDictList[newYDataList[0][1].currentIndex()])
               # xMax = float(max(xNoNoneArray))
               # xMin = float(min(xNoNoneArray))
               # yMax = float(max(yNoNoneArray))
               # yMin = float(min(yNoNoneArray))
               #
               # print(xMax)
               # print(yMax)

               if len(newYDataList) > 1:
                   # for i in newYDataList:
                   #     y = np.array()
                   drawSinglePlotWithParameterInGui()
                   # 从本地读图
                   pixmap = QPixmap('preview.png')  # 按指定路径找到图片
                   print(pixmap.size())
                   if pixmap:
                       print('!!!!!!!!!!')

                   else:
                       pass

                   previewDialogController.previewDialog = previewDialog()
                   previewDialogController.previewDialog.resizeDialog(pixmap.size().width(), pixmap.size().height())
                   previewDialogController.previewDialog.setPreviewImg(pixmap)
                   previewDialogController.previewDialog.show()
                   QMessageBox.information(MainWindow,'!!!!','~~~~~~~~~')
               else:
                   #绘制单图模式！！！
                   drawSinglePlotWithParameterInGui()
                    # 从本地读图
                   pixmap = QPixmap('preview.png')  # 按指定路径找到图片
                   print(pixmap.size())
                   if pixmap:
                     print('!!!!!!!!!!')

                   else:
                       pass

                   previewDialogController.previewDialog = previewDialog()
                   previewDialogController.previewDialog.resizeDialog(pixmap.size().width(), pixmap.size().height())
                   previewDialogController.previewDialog.setPreviewImg(pixmap)
                   previewDialogController.previewDialog.show()

       else:
           QMessageBox.information(MainWindow,'警告！！', '请先导入数据源！！')

    def savePushButtonClicked(self):
        self.thread_4 = Thread_4()
        self.thread_4._savePictureSignal.connect(self.setSaveButtonEnable)
        self.thread_4.start()
        self.savePicture()

    def addYDataButtonClicked(self):
        print("增加Y轴！！！")
        global newYDataList
        global tableHeaderList
        # if len(newYDataList) == 0:
        #     print('当前无新增Y轴')
        # else:
        #     for i in newYDataList:
        currentIndexStr = str(len(newYDataList) + 1)

        #yLabel
        yLabel = QLabel(QtWidgets.QFrame(self.y1Label))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(yLabel.sizePolicy().hasHeightForWidth())
        yLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe Arabic")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        yLabel.setFont(font)
        yLabel.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                   "border-radius:5px;\n"
                                   "color:#000;\n"
                                   "border: 0px solid #000")
        yLabel.setObjectName('y'+currentIndexStr+'Label')
        yLabel.setText('y'+currentIndexStr+'轴')
        print(yLabel.objectName())
        self.mainGridLayout.addWidget(yLabel,len(newYDataList)+1+6,0,1,1)

        #yComboBox
        yComboBox = QtWidgets.QComboBox(QtWidgets.QFrame(self.y1ComboBox))
        yComboBox.setObjectName('y' + currentIndexStr + 'ComboBox')
        yComboBox.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                  "border-radius:5px;\n"
                                  "color:#000;\n"
                                  "border: 1px solid #000")

        print(yComboBox.objectName())
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(yComboBox.sizePolicy().hasHeightForWidth())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(yComboBox.sizePolicy().hasHeightForWidth())
        yComboBox.setSizePolicy(sizePolicy)
        yComboBox.setMinimumSize(QtCore.QSize(120, 30))
        yComboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        yComboBox.setMinimumContentsLength(10)
        self.mainGridLayout.addWidget(yComboBox, len(newYDataList) + 1 + 6, 1, 1, 1)
        yComboBox.activated[str].connect(self.YComboBoxValueChanged)
        if len(tableHeaderList)>0 :
            yComboBox.removeItem(0)
            yComboBox.addItems(tableHeaderList)
        else:
            yComboBox.addItem('y' + currentIndexStr + '轴')


        #yTitleTextEdit
        yTitleTextEdit = QtWidgets.QTextEdit(QtWidgets.QFrame(self.y1TitleTextEdit))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(yTitleTextEdit.sizePolicy().hasHeightForWidth())
        yTitleTextEdit.setSizePolicy(sizePolicy)
        yTitleTextEdit.setMinimumSize(QtCore.QSize(130, 30))
        yTitleTextEdit.setMaximumSize(QtCore.QSize(130, 30))
        # yTitleTextEdit.setBaseSize(QtCore.QSize(40, 0))
        yTitleTextEdit.setObjectName('y' + currentIndexStr + 'TitleTextEdit')
        yTitleTextEdit.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                        "border-radius:5px;\n"
                                        "color:#000;\n"
                                        "border: 1px solid #000")
        yTitleTextEdit.setText('y' + currentIndexStr + '轴标题')
        print(yTitleTextEdit.objectName())
        self.mainGridLayout.addWidget(yTitleTextEdit, len(newYDataList) + 1 + 6, 2, 1, 1)


        #self.y1LineTypeComboBox
        yLineTypeComboBox = QtWidgets.QComboBox(QtWidgets.QFrame(self.y1LineTypeComboBox))
        yLineTypeComboBox.setObjectName('y' + currentIndexStr + 'LineTypeComboBox')
        yLineTypeComboBox.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                "border-radius:5px;\n"
                                "color:#000;\n"
                                "border: 1px solid #000")
        print(yLineTypeComboBox.objectName())
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(yComboBox.sizePolicy().hasHeightForWidth())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(yLineTypeComboBox.sizePolicy().hasHeightForWidth())
        yLineTypeComboBox.setSizePolicy(sizePolicy)
        yLineTypeComboBox.setMinimumSize(QtCore.QSize(120, 30))
        yLineTypeComboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        yLineTypeComboBox.setMinimumContentsLength(10)
        yLineTypeComboBox.addItem("实线 -")
        yLineTypeComboBox.addItem("点虚线 :")
        yLineTypeComboBox.addItem("破折线 --")
        yLineTypeComboBox.addItem("点划线 -.")
        yLineTypeComboBox.addItem("不画线 ")
        self.mainGridLayout.addWidget(yLineTypeComboBox, len(newYDataList) + 1 + 6, 3, 1, 1)

        #yLineWidthDoubleSpinBox
        yLineWidthDoubleSpinBox = QtWidgets.QDoubleSpinBox(QtWidgets.QFrame(self.y1LineWidthDoubleSpinBox))
        yLineWidthDoubleSpinBox.setValue(1.0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(yLineWidthDoubleSpinBox.sizePolicy().hasHeightForWidth())
        yLineWidthDoubleSpinBox.setSizePolicy(sizePolicy)
        yLineWidthDoubleSpinBox.setMinimumSize(QtCore.QSize(40, 30))
        yLineWidthDoubleSpinBox.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                                    "border-radius:5px;\n"
                                                    "color:#000;\n"
                                                    "border: 1px solid #000")
        yLineWidthDoubleSpinBox.setObjectName('y' + currentIndexStr + 'LineWidthDoubleSpinBox')
        print(yLineWidthDoubleSpinBox.objectName())
        self.mainGridLayout.addWidget(yLineWidthDoubleSpinBox, len(newYDataList) + 1 + 6, 4, 1, 1)


        #yLineColorPushButton
        yLineColorPushButton = QtWidgets.QPushButton(QtWidgets.QFrame(self.y1LineColorPushButton))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(yLineColorPushButton.sizePolicy().hasHeightForWidth())
        yLineColorPushButton.setSizePolicy(sizePolicy)
        yLineColorPushButton.setMinimumSize(QtCore.QSize(120, 30))
        yLineColorPushButton.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                                 "border-radius:5px;\n"
                                                 "color:#000;\n"
                                                 "border: 1px solid #000")
        yLineColorPushButton.setObjectName('y' + currentIndexStr + 'LineColorPushButton')
        print(yLineColorPushButton.objectName())
        # yLineColorPushButton.setText('连线颜色')
        yLineColorPushButton.setText('#000000')
        yLineColorPushButton.setStyleSheet('QWidget {background-color:#000000}')
        yLineColorPushButton.clicked.connect(self.lineColorPushButtonClicked)
        self.mainGridLayout.addWidget(yLineColorPushButton, len(newYDataList) + 1 + 6, 5, 1, 1)

        #yMaxYLineEdit
        yMaxYLineEdit = QtWidgets.QLineEdit(QtWidgets.QFrame(self.y1MaxYLineEdit))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(yMaxYLineEdit.sizePolicy().hasHeightForWidth())
        yMaxYLineEdit.setSizePolicy(sizePolicy)
        yMaxYLineEdit.setMinimumSize(QtCore.QSize(40, 30))
        yMaxYLineEdit.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                          "border-radius:5px;\n"
                                          "color:#000;\n"
                                          "border: 1px solid #000")
        yMaxYLineEdit.setObjectName('y' + currentIndexStr + 'MaxYLineEdit')
        yMaxYLineEdit.setText('最大值')
        print(yMaxYLineEdit.objectName())
        self.mainGridLayout.addWidget(yMaxYLineEdit, len(newYDataList) + 1 + 6, 6, 1, 1)

        #yMinYLineEdit
        yMinYLineEdit = QtWidgets.QLineEdit(QtWidgets.QFrame(self.y1MinYLineEdit))
        yMinYLineEdit.setMinimumSize(QtCore.QSize(40, 30))
        yMinYLineEdit.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                          "border-radius:5px;\n"
                                          "color:#000;\n"
                                          "border: 1px solid #000")
        yMinYLineEdit.setObjectName('y' + currentIndexStr + 'MinYLineEdit')
        yMinYLineEdit.setText('最小值')
        print(yMinYLineEdit.objectName())
        self.mainGridLayout.addWidget(yMinYLineEdit, len(newYDataList) + 1 + 6, 7, 1, 1)

        #yStepLineEdit
        yStepLineEdit = QtWidgets.QLineEdit(QtWidgets.QFrame(self.y1StepLineEdit))
        yStepLineEdit.setMinimumSize(QtCore.QSize(40, 30))
        yStepLineEdit.setStyleSheet("font: 75 14pt \"Adobe Arabic\";\n"
                                          "border-radius:5px;\n"
                                          "color:#000;\n"
                                          "border: 1px solid #000")
        yStepLineEdit.setObjectName('y' + currentIndexStr + 'StepLineEdit')
        yStepLineEdit.setText('步长')
        self.mainGridLayout.addWidget(yStepLineEdit, len(newYDataList) + 1 + 6, 8, 1, 1)


        # self.mainGridLayout.setContentsMargins(1, 1, 1, 1)
        self.mainGridLayout.addWidget(self.addYpushButton, len(newYDataList) + 1 + 6 + 2, 0, 1, 1)
        self.mainGridLayout.addWidget(self.deleteYPushButton, len(newYDataList) + 1 + 6 + 3, 0, 1, 1)
        newYDataList.append([yLabel,
                             yComboBox,
                             yTitleTextEdit,
                             yLineTypeComboBox,
                             yLineWidthDoubleSpinBox,
                             yLineColorPushButton,
                             yMaxYLineEdit,
                             yMinYLineEdit,
                             yStepLineEdit])
        print('当前新增y轴数为%d'%len(newYDataList))
        print('新增y轴分别为', newYDataList)
        # newYDataList.append(str(len(newYDataList)+2))
        # self.adaptYEdit()
        # self.adaptYTitle()


    def deleteYDataButtonClicked(self):
        global newYDataList
        if len(newYDataList) > 1:
            for i in newYDataList[-1]:
                self.mainGridLayout.removeWidget(i)
            newYDataList.pop(-1)
            print("删除了1个数据，还剩下新增Y轴",newYDataList)

        else:
            QMessageBox.information(MainWindow,"警告！！！","最少有一个Y轴！！！")
    def XComboBoxValueChanged(self):
        print('X轴改变了！！！')
        self.adaptXEdit()
        self.adaptXTitle()


    def YComboBoxValueChanged(self):
        print('Y轴改变了！！！')
        self.adaptYEdit()
        self.adaptYTitle()

    def showDialog(self):
        col = QColorDialog.getColor()
        print(col.name(), "\n")
        if col.isValid():
            self.sender().setStyleSheet('QWidget {background-color:%s}' % col.name())
            self.sender().setText(col.name())



    def getDataFromTableWidget(self):
        global dataDictKey
        global dataDictList
        dataDictList.clear()
        dataDictKey.clear()
        # dataDictList.append([0,1,2])
        rowCount = self.dataTableWidget.rowCount()
        columnCount = self.dataTableWidget.columnCount()
        #print(self.dataTableWidget_2.item(0,0).text())
        #print(dataDictKey)
        i = 0
        while i < columnCount:
            columnDataList = []
            j = 0
            while j < rowCount:
                columnDataList.append(self.dataTableWidget.item(j, i).text())
                j = j + 1
            dataDictList.append(columnDataList)
            #print(dataDictList)
            i= i+1

        #
        # for i in columnCount:
        #     for j in rowCount:
        #        columnDataList = columnDataList.append(self.dataTableWidget_2.item(j,i))
        #     dataDictList = dataDictList.append({i:columnDataList})
        print(dataDictList)

    def setSelectFileButtonEnable(self):
        self.selectFileButton.setEnabled(True)

    def setLineColorPushButtonEnable(self):
        self.y1LineColorPushButton.setEnabled(True)

    def setPreviewButtonEnable(self):
        self.previewPushButton.setEnabled(True)

    def setSaveButtonEnable(self):
        self.savePushButton.setEnabled(True)

    def showPreviewView(self):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(845, 536)
        MainWindow.setStyleSheet("")
        MainWindow.setAnimated(True)

    def savePicture(self):
        global figList
        if len(figList) > 0:
            fig = figList[0]
            fdir, ftype = QFileDialog.getSaveFileName(self,
                                                      "Save Image",
                                                      "./",
                                                      "Image Files (*.jpg)")
            fig.savefig(fdir, bbox_inches='tight')
            print(fdir)
        else:
            QMessageBox.information(MainWindow,
                                    '警告！！',
                                    '你还未绘制图片！！')

    def adaptXEdit(self):
        global xDataList
        if len(dataDictList) > 0:
            xArray = dataDictList[xDataList[0][1].currentIndex()]
            xFloatArray = []
            for n in xArray:
                xFloatArray.append(float(n))
            xMax = float(max(xFloatArray))
            xMin = float(min(xFloatArray))
            print(str(xMax) + '!!!!!!!!!!!!!!!!!!')
            xStep = myArangeUtil.caculateUnitStep(xMax, xMin)
            xDataList[0][3].setText(str(xMax))
            xDataList[0][4].setText(str(xMin))
            xDataList[0][5].setText(str(xStep))
        else:
            QMessageBox.information(MainWindow, '警告！！！', '没有可用数据源！！！')

    def adaptYEdit(self):
        # 根据点击按钮事件，计算出建议的最大x、y分别的最大值，最小值和步长
        global newYDataList
        if len(dataDictList) > 0:
            #第一次点击选择导入数据源时需要给初始Y轴填入数据
            if self.sender().objectName() == 'selectFileButton':
                yArray = dataDictList[newYDataList[0][1].currentIndex()]
                yFloatArray = []
                for m in yArray:
                    yFloatArray.append(float(m))
                yMax = float(max(yFloatArray))
                yMin = float(min(yFloatArray))
                yStep = myArangeUtil.caculateUnitStep(yMax, yMin)
                newYDataList[0][6].setText(str(yMax))
                newYDataList[0][7].setText(str(yMin))
                newYDataList[0][8].setText(str(yStep))
            else:
                indexStr = self.sender().objectName()[1]
                print('-------------' + indexStr + '!!!!!!!!!!!!!!')
                yArray = dataDictList[newYDataList[int(indexStr) - 1][1].currentIndex()]
                yFloatArray = []
                for m in yArray:
                    yFloatArray.append(float(m))
                yMax = float(max(yFloatArray))
                yMin = float(min(yFloatArray))
                yStep = myArangeUtil.caculateUnitStep(yMax, yMin)
                newYDataList[int(indexStr) - 1][6].setText(str(yMax))
                newYDataList[int(indexStr) - 1][7].setText(str(yMin))
                newYDataList[int(indexStr) - 1][8].setText(str(yStep))
            # else:
            #     #至少有一个y轴，在点击导入按钮时响应，导入文件后需要显示出数据！！！
            #     yArray = dataDictList[self.y1ComboBox.currentIndex()]
            #     yFloatArray = []
            #     for m in yArray:
            #         yFloatArray.append(float(m))
            #     yMax = float(max(yFloatArray))
            #     yMin = float(min(yFloatArray))
            #     print(str(yMax) + '~~~~~~~~~~~~~~~~~~')
            #     yStep = myArangeUtil.caculateUnitStep(yMax, yMin)
            #     self.y1MaxYLineEdit.setText(str(yMax))
            #     self.y1MinYLineEdit.setText(str(yMin))
            #     self.y1StepLineEdit.setText(str(yStep))


        else:
            QMessageBox.information(MainWindow,'警告！！！','没有可用数据源！！！')

    def adaptXTitle(self):
        xDataList[0][2].setPlainText(xDataList[0][1].currentText())

    def adaptYTitle(self):
        global newYDataList
        # self.y1TitleTextEdit.setPlainText(self.y1ComboBox.currentText())
        if len(newYDataList) > 0 :
            for i in newYDataList:
                i[2].setPlainText(i[1].currentText())


def currentLineStyle(currentIndex:int)->str:
    # 'solid'(默认) '-' 实线
    # 'dotted' ':' 点虚线
    # 'dashed' '--' 破折线
    # 'dashdot' '-.' 点划线
    # 'None' '' 或 ' ' 不画线
    if currentIndex == 0:
        return 'solid'
    elif currentIndex == 1:
        return 'dotted'
    elif currentIndex == 2:
        return 'dashed'
    elif currentIndex == 3:
        return 'dashdot'
    elif currentIndex == 4:
        return 'None'
    elif currentIndex == 5:
        return 'solid'


def handlerUnlegalData(xArray:list,
                       yArray:list):
    xNoNoneArray = []
    yNoNoneArray = []
    # xArray = [round(float(i)) for i in xArray]
    print(xArray)
    for i in xArray:
        try:
            xNoNoneArray.append(round(float(i)))
        except:
            print('x轴存在无法转换为数字的项目！！！')
            xNoNoneArray.append(0.0)
        else:
            print('当前转化成功！！！')
        finally:
            print('全部转化成功！！！')
    for n in yArray:
        try:
            yNoNoneArray.append(round(float(n)))
        except:
            yNoNoneArray.append(0.0)
            print('由于参数为非数字已强制转为0.0')
        else:
            print('当前转化成功！！！')
        finally:
            print('全部转化成功！！！')
    return xNoNoneArray,yNoNoneArray


def drawSinglePlotWithParameterInGui():
    global xDataList
    global newYDataList
    global figLi

    figList.clear()
    #plt.figure(figsize=(float(picWidth)/float(picDPI), float(picHeight)/float(picDPI)), dpi=float(picDPI))
    #plt.figure(dpi=float(picDPI))
    plt.figure(figsize=(int(float(xDataList[0][6].text())/float(xDataList[0][8].text())),
                        int(float(xDataList[0][7].text())/float(xDataList[0][8].text()))),
               dpi=int(xDataList[0][8].text()))

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # plt.rcParams['font.size'] = 20  # 设置字体大小




    plt.subplot(1,1,1)

    #titleTextEdit富文本设置坐标轴名称
    plt.xlabel(xlabel=xDataList[0][2].toPlainText())
    plt.xticks(np.arange(0,
                         (float(xDataList[0][3].text()) + myArangeUtil.caculateUnitStep(float(xDataList[0][3].text()), float(xDataList[0][4].text()))),
                         step=float(xDataList[0][5].text())),
               np.arange(0, (float(xDataList[0][3].text()) + myArangeUtil.caculateUnitStep(float(xDataList[0][3].text()), float(xDataList[0][4].text()))),
                         step=float(xDataList[0][5].text())))
    for i in newYDataList:
        xNoNoneArray, yNoNoneArray = handlerUnlegalData(dataDictList[xDataList[0][1].currentIndex()],
                                                        dataDictList[i[1].currentIndex()])
        x = np.array(xNoNoneArray)
        y = np.array(yNoNoneArray)
        plt.yticks(np.arange(0,
                             float(i[6].text()) + myArangeUtil.caculateUnitStep(float(i[6].text()), float(i[7].text())),
                             step=float(i[8].text())),
                   np.arange(0,
                             float(i[6].text()) + myArangeUtil.caculateUnitStep(float(i[6].text()), float(i[7].text())),
                             step=float(i[8].text())))
        plt.ylabel(ylabel=i[2].toPlainText())
        plt.plot(x,
                 y,
                 color=i[5].text(),
                 linewidth=i[4].text(),
                 linestyle=currentLineStyle(i[3].currentIndex()))

    # plt.yticks(np.arange(0,
    #                      (float(newYDataList[0][6].text()) + myArangeUtil.caculateUnitStep(
    #                          float(newYDataList[0][6].text()), float(newYDataList[0][7].text()))),
    #                      step=float(newYDataList[0][8].text())),
    #            np.arange(0, (float(newYDataList[0][6].text()) + myArangeUtil.caculateUnitStep(
    #                float(newYDataList[0][6].text()), float(newYDataList[0][7].text()))),
    #                      step=float(newYDataList[0][8].text())))
    #plt.yticks(np.linspace(0,maxY,yUnitNum))

    #plt.xticks(rotation = '90')
    #plt.yticks(rotation='90')



    ax = plt.gca()
    ax.set_ylim(0)
    ax.set_xlim(0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')  # 将y轴的位置设置在右左边
    #ax.invert_yaxis()  # y轴反向
    #ax.invert_xaxis()
    #plt.suptitle("RUNOOB subplot Test")
    fig = plt.gcf()
    figList.append(fig)

    plt.savefig('preview.png')
    #plt.scatter([-y for y in yArray], xArray)
    plt.show()




qmut_1 = QMutex() # 创建线程锁
qmut_2 = QMutex()
# 继承QThread
class Thread_1(QThread):  # 线程1
    def __init__(self):
        super().__init__()

    def run(self):
        qmut_1.lock() # 加锁
        values = [1, 2, 3, 4, 5]
        for i in values:
            print(i)
            time.sleep(0.5)  # 休眠
        qmut_1.unlock() # 解锁


class Thread_2(QThread):  # 线程2
    _signal =pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        # qmut_2.lock()  # 加锁
        values = ["a", "b", "c", "d", "e"]
        for i in values:
            print(i)
            time.sleep(0.5)
        # qmut_2.unlock()  # 解锁
        self._signal.emit()

class Thread_3(QThread):  # 线程3
    _reloadUISignal =pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        # qmut_2.lock()  # 加锁
        values = ["a", "b", "c", "d", "e"]
        for i in values:
            print(i)
            time.sleep(0.5)
        # qmut_2.unlock()  # 解锁
        self._reloadUISignal.emit()


class Thread_4(QThread):  # 线程4
    _savePictureSignal =pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        # qmut_2.lock()  # 加锁
        values = ["a", "b", "c", "d", "e"]
        for i in values:
            print(i)
            time.sleep(0.5)
        # qmut_2.unlock()  # 解锁
        self._savePictureSignal.emit()



class Thread_5(QThread):  # 线程2
    _selectColorSignal =pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        # qmut_2.lock()  # 加锁
        values = ["a", "b", "c", "d", "e"]
        for i in values:
            print(i)
            time.sleep(0.5)
        # qmut_2.unlock()  # 解锁
        self._selectColorSignal.emit()

#---------------------------------------------------------------------------------

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = window()  # 创建窗体对象
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程


