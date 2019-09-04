from test import Ui_CamShow
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
from PyQt5.QtCore import QTimer,QCoreApplication
from PyQt5.QtGui import QPixmap
import cv2
import qimage2ndarray
import time
import pyqtgraph as py
import numpy as np
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import Qt,QRect


class CamShow(QMainWindow,Ui_CamShow):
    def __init__(self,parent=None):
        super(CamShow,self).__init__(parent)
        self.setupUi(self)
        self.PrepWidgets()
        self.PrepParameters()
        self.Timer = QTimer(self)
        
        self.CallBackFunctions()
        
        #self.Timer.timeout.connect(self.TimerOutFun)
        
        self.stopbt = 0
        #self.draw.plotItem.showGrid(True, True, 0.7)
        

    #控件初始化
    def PrepWidgets(self):
        self.PrepCamera()
        self.StopBt.setEnabled(False)
        self.RecordBt.setEnabled(False)

    def PrepCamera(self):
        self.camera=cv2.VideoCapture(0)
  

    def PrepParameters(self):
        self.RecordFlag=0
        self.RecordPath='D:/Python/PyQt/'
        self.FilePathLE.setText(self.RecordPath)
        self.Image_num=0
        

    def CallBackFunctions(self):
        self.FilePathBt.clicked.connect(self.SetFilePath)
        self.ShowBt.clicked.connect(self.StartCamera)
        self.StopBt.clicked.connect(self.StopCamera)
        self.RecordBt.clicked.connect(self.RecordCamera)
        self.ExitBt.clicked.connect(self.ExitApp)
        self.Timer.timeout.connect(self.TimerOutFun)
        #self.btnAdd.clicked.connect(self.update)
        #self.btnAdd.clicked.connect(self.drawAvg)
        
        

    def StartCamera(self):
        self.ShowBt.setEnabled(False)
        self.StopBt.setEnabled(True)
        self.RecordBt.setEnabled(True)
        self.RecordBt.setText('Record')
        self.Timer.start(1)
        t1=time.clock()
        points=100
        X= np.arange(points)
        Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        C=py.hsvColor(time.time()/5%1,alpha=.5)
        pen=py.mkPen(color=C,width=10)
        #self.draw.plot(X,Y,pen=pen,clear=True)
        #print("update took %.02f ms"%((time.clock()-t1)*1000))
       # QtCore.QTimer.singleShot(1, self.StartCamera) # QUICKLY repeat 1毫秒執行一次
        

    def StopCamera(self):
        if self.StopBt.text() == 'Stop':
            self.StopBt.setText('Continue')
            #self.stopbt = 0
            self.RecordBt.setText('Save Pic')
            self.Timer.stop()
        else:
            self.StopBt.setText('Stop')
            #self.stopbt = 1
            self.RecordBt.setText('Record')
            self.Timer.start(1)


    def TimerOutFun(self):
        success,self.img=self.camera.read()
        
       # print(self.Timer.time())
        self.gray = cv2.cvtColor(self.img,cv2.COLOR_RGB2GRAY)
        if success:   
            self.DispImg()
            self.CopyImg()
            self.drawAvg()
          #  print(np.sum(self.img))
           # print(self.img)             
            #self.Image_num+=1
            #inputImg = cv2.imread(self.img)
            """
            img2RGB = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
            #初始化numpy arr
            r_arr = np.zeros((500,1) , np.float16)
            g_arr = np.zeros((500,1) , np.float16)
            b_arr = np.zeros((500,1) , np.float16)

            for i in range(500):
                r_arr[i,0] = np.sum(img2RGB[10:20 , i , 0]) / 10
                g_arr[i,0] = np.sum(img2RGB[10:20 , i , 1]) / 10
                b_arr[i,0] = np.sum(img2RGB[10:20 , i , 2]) /10
            
            x = np.linspace(0,500,500)       
            self.draw_2.plot(x, r_arr[:,0] , pen='r')
            self.draw_2.plot(x, g_arr[:,0] , pen='g')
            self.draw_2.plot(x, b_arr[:,0] , pen='b')
         
"""
            if self.RecordFlag:
                self.video_writer.write(self.img)

    
                       
    
    def DispImg(self):
        CVimg = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(CVimg)
        self.DispLb.setPixmap(QPixmap(qimg))
        self.DispLb.show()

    def CopyImg(self):
        ret=QRect(50,200,411,10)       
        CVimg = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)       
        qimg = qimage2ndarray.array2qimage(CVimg)
        b=qimg.copy(ret)

        self.DispCopyImg.setPixmap(QPixmap(b))
        self.DispCopyImg.show()

    
    def SetFilePath(self):
        dirname = QFileDialog.getExistingDirectory(self, "瀏覽", '.')
        if dirname:

            self.FilePathLE.setText(dirname)
            self.RecordPath=dirname+'/'

    def RecordCamera(self):
        tag=self.RecordBt.text()
        if tag=='Save Pic':
            image_name=self.RecordPath+'self.image'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.jpg'
            print(image_name)
            cv2.imwrite(image_name,self.img)
            
        elif tag =='Record':
            self.RecordBt.setText('Stop')
            video_name = self.RecordPath + 'video' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.avi'
            size = (self.img.shape[1],self.img.shape[0])
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.video_writer = cv2.VideoWriter(video_name, fourcc,self.camera.get(5), size)
            self.RecordFlag=1
            self.StopBt.setEnabled(False)
            self.ExitBt.setEnabled(False)

        elif tag == 'Stop':
            self.RecordBt.setText('Record')
            self.video_writer.release()
            self.RecordFlag = 0
            self.StopBt.setEnabled(True)
            self.ExitBt.setEnabled(True)

    """
    def update(self):
        t1=time.clock()
        points=100
        X= np.arange(points)
        Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        C=py.hsvColor(time.time()/5%1,alpha=.5)
        pen=py.mkPen(color=C,width=10)
        self.draw.plot(X,Y,pen=pen,clear=True)
        #print("update took %.02f ms"%((time.clock()-t1)*1000))
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat """

    def drawAvg(self):
        self.draw_2.clear()
        #inputImg= cv2.imread(self.img)
        #img = cv2.imread('rgb.png')
        img2RGB = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        #初始化numpy arr
        r_arr = np.zeros((640,1) , np.uint8)
        g_arr = np.zeros((640,1) , np.uint8)
        b_arr = np.zeros((640,1) , np.uint8)
        for i in range(640):
            #print(np.sum(self.img[10:20 , i , 0] ))
            r_arr[i,0] = np.sum(img2RGB[100:110 , i , 0] )/ 10
            g_arr[i,0] = np.sum(img2RGB[100:110 , i , 1] )/ 10
            b_arr[i,0] = np.sum(img2RGB[100:110 , i , 2] )/ 10
        #rint(r_arr[0,0])

        x = np.linspace(0,640,640)
        self.draw_2.setRange(xRange=[0,640]) # 固定x軸 不會拉動
        self.draw_2.setRange(yRange=[0,255]) # 固定y軸 不會拉動
   
        self.draw_2.plot(x, r_arr[:,0] , pen='r')
        self.draw_2.plot(x, g_arr[:,0] , pen='g')
        self.draw_2.plot(x, b_arr[:,0] , pen='b')
        
       

    def ExitApp(self):
        self.Timer.Stop()
        self.camera.release()
        QCoreApplication.quit()
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui=CamShow()
    ui.show()
    app.exec_()
    print(self.StopBt.setText())
