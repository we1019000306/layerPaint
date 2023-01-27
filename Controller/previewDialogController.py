import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5 import QtCore, QtWidgets
from layerPaint.View.previewDialog import Ui_Dialog


class previewDialog(QtWidgets.QMainWindow,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #设置主界面的标题及初始大小
        self.setWindowTitle('Dialog')
        self.resize(350,300)
        # 设置按钮的属性：文本，移动位置，链接槽函数
        self.previewLabel.resize(self.size().width(),self.size().height())


    def resizeDialog(self,width:int,height:int):
        #创建QDialog对象
        screenDesktop = QApplication.desktop()
        screenRect = screenDesktop.screenGeometry()
        screenHeight = int(screenRect.height())
        screenWidth = int(screenRect.width())
        self.resize(screenWidth,screenHeight)
        self.previewLabel.resize(width,height)
        self.previewLabel.move(int((screenWidth-width)/2),int((screenHeight-height)/2))
        #设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面


    def setPreviewImg(self,QPixmap):
        self.previewLabel.setPixmap(QPixmap)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=previewDialog()
    demo.resizeDialog(500,500)
    demo.show()
    sys.exit(app.exec_())