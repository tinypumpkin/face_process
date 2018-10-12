# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import time
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QLineEdit, QInputDialog, QComboBox, QLabel, QFileDialog, QSplashScreen)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui  import *
from PyQt5.QtCore import * 
from Ui_Main import Ui_MainWindow
import subprocess
import process_pic
import pic_face_process
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.path=''
        self.bool=0
        self.child=0
        self.click=" "
    
    @pyqtSlot()
    def on_action_11_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        exit(0)
        
    
    @pyqtSlot()
    def on_action_5_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print('最小化')
        self.showMinimized()
    
    @pyqtSlot()
    def on_action_9_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print('全屏')
        self.showFullScreen()

    
    @pyqtSlot()
    def on_action_10_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.showNormal()

    
    @pyqtSlot()
    def on_action_QT_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        button=QMessageBox.aboutQt(self, '介绍Qt')
    
    @pyqtSlot()
    def on_action_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        button=QMessageBox.about(self, '介绍此软件', '此软件是用python语言开发，主要用到Dlib，opencv，pyqt5 三种库利用计算机视觉技术进行图像处理从而识别目标对象表情')
    


    
    @pyqtSlot()
    def on_action_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        button=QMessageBox.about(self, '帮助','这只是个摆设23333') 

    @pyqtSlot()
    def on_action_12_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        button=QMessageBox.about(self, '注意', '此软件只可接受png/jpg格式图片输出统一格式为png')


    #打开图片
    @pyqtSlot()
    def on_action_3_triggered(self):
        """
        Slot documentation goes here.
        """
        png, pictuer=QFileDialog.getOpenFileName(self, '打开图片', '/', '*.jpg *.png')
        self.path=str(png)
        print(self.path)
#此处开始是保存到本地的操作
        pic=open(self.path, 'rb')
        g=pic.read()
        f=open(str(os.path.abspath('.'))+"\str.png",'wb')
        f.write(g)
        pic.close()
        f.close()
#此次保存到本地完成
        pixMap = QPixmap(str(png)).scaled(self.label.width(),self.label.height())
        self.label.setPixmap(pixMap)

    
    @pyqtSlot()
    def on_action_4_triggered(self):
        """
        Slot documentation goes here.
        """
        try:
            if self.click=="process":
                self.on_pushButton_2_clicked()
            if self.click=="face_r":
                self.on_pushButton_clicked()
            path, my_file=QFileDialog.getSaveFileName(self, '存储为', '/', '*.png')
            print(path)
            pic=open("temp.png", 'rb')
            g=pic.read()
            
            
            f=open(path, 'wb')
            f.write(g)
            pic.close()
            f.close()
        except:
            button=QMessageBox.about(self, '注意', '操作后再保存')
        else:
            pass

    
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            if self.click=="process":
                self.on_pushButton_2_clicked()
            if self.click=="face_r":
                self.on_pushButton_clicked()
            path, my_file=QFileDialog.getSaveFileName(self, '存储为', '/', '*.png')
            print(path)
            pic=open(self.click, 'rb')
            g=pic.read()
            
            
            f=open(path, 'wb')
            f.write(g)
            pic.close()
            f.close()
        except:
            button=QMessageBox.about(self, '注意', '操作后再保存')
        else:
            pass
        
    
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.bool==0:
            self.bool=1
            self.pushButton_3.setText("关闭实时表情识别")
            #try_emotion.face_emotion().learning_face()
            #print ( '当前id是', os.getpid () )
            self.chind=subprocess.Popen('python try_emotion.py')#开启实时情绪识别
            
            
        else:
            self.bool=0
            #try_emotion.count=1
            self.pushButton_3.setText("实时表情识别")
            #print('try_emotion的是',try_emotion.face_emotion().pid())
            self.chind.kill()
        
        
    #此处是process_pic生成
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            str='str.png'
            process_pic.graphics ().process (str)
            self.click="process"
            pixMap = QPixmap("temp.png").scaled(self.label.width(),self.label.height())
            self.label.setPixmap(pixMap)
        except:
            button=QMessageBox.about(self, '注意', '应先向空白处导入图片后再进行处理')
        else:
            pass



        #os.popen('python process_pic.py')


    #此处是图片面部识别
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            str='str.png'
            pic_face_process.face_emotion().learning_face(str)
            self.click="face_r"
            pixMap = QPixmap("temp.png").scaled(self.label.width(),self.label.height())
            self.label.setPixmap(pixMap)
        except:
            button=QMessageBox.about(self, '注意', '应先向空白处导入图片后再进行处理')
        else:
            pass
'''
class MovieSplashScreen(QSplashScreen):

    def __init__(self, movie, parent = None):
        movie.jumpToFrame(0)
        pixmap = QPixmap(movie.frameRect().size())
        QSplashScreen.__init__(self, pixmap)
        self.movie = movie
        self.movie.frameChanged.connect(self.repaint)
    
    def showEvent(self, event):
        self.movie.start()
    
    def hideEvent(self, event):
        self.movie.stop()
    
    def paintEvent(self, event):
    
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        self.setMask(pixmap.mask())
        painter.drawPixmap(0, 0, pixmap)
    
    def sizeHint(self):
        return self.movie.scaledSize()
'''


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
#    movie = QMovie("begin.gif")
#    splash = MovieSplashScreen(movie)
    #splash.show()
    #splash=QSplashScreen(QPixmap("1.png"))    #没什么用的启动界面就是用来装逼的
    #splash.show()
    #splash.showMessage('正在初始化...')
    #time.sleep(1)
    #splash.showMessage('正在加载文件请稍后...')
    #time.sleep(1)
    app.processEvents()
    ui=MainWindow()
    ui.show()
    #splash.finish(ui)
    sys.exit(app.exec_())
