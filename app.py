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
        self.Exposure.setEnabled(False)

    def PrepCamera(self):
        self.camera=cv2.VideoCapture(0)
        #self.camera.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        #self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        #self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE,0.25)
        #self.camera.set(cv2.CAP_PROP_EXPOSURE,float(0.1))
        #self.camera.set(cv2.CAP_PROP_ISO_SPEED,100)
  

    def PrepParameters(self):
        self.RecordFlag=0 # 0=not save video, 1=save
        self.RecordPath='D:/Python/PyQt/'
        self.FilePathLE.setText(self.RecordPath)
        self.Image_num=0
        self.Exposure.currentIndexChanged.connect(lambda:self.camera.get(15))
        self.SetExposure()

        

    def CallBackFunctions(self):
        self.FilePathBt.clicked.connect(self.SetFilePath)
        self.ShowBt.clicked.connect(self.StartCamera)
        self.StopBt.clicked.connect(self.StopCamera)
        self.RecordBt.clicked.connect(self.RecordCamera)
        self.ExitBt.clicked.connect(self.ExitApp)
        self.Timer.timeout.connect(self.TimerOutFun)
        self.BtnGo.clicked.connect(self.calculate)
        self.Exposure.activated.connect(self.SetExposure)
       

    def SetExposure(self):
        exposure_time = float(self.Exposure.currentText())
        print(exposure_time)
        self.camera.set(15,exposure_time)

              

    def StartCamera(self):
        self.ShowBt.setEnabled(False)
        self.StopBt.setEnabled(True)
        self.RecordBt.setEnabled(True)
        self.Exposure.setEnabled(True)
        self.GrayCheck.setEnabled(True)
        self.RecordBt.setText('Record')
        self.Timer.start(1)
        
    

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

        if self.GrayCheck.isChecked():
            self.GrayImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        
       # print(self.Timer.time())
        
        if success:   
            self.DispImg()
            self.CopyImg()
            self.drawAvg()
          #  print(np.sum(self.img))
           # print(self.img)             
            #self.Image_num+=1
            #inputImg = cv2.imread(self.img)
            
            if self.RecordFlag:
                if self.GrayCheck.isChecked():
                    color = cv2.cvtColor(self.GrayImg, cv2.COLOR_GRAY2RGB) #再轉換一次灰階到彩色才會有三通到，儲存影片才能成功
                    self.video_writer.write(color)
                else:
                    self.video_writer.write(self.img)
                
                   
    
    def DispImg(self):
        if self.GrayCheck.isChecked():
            qimg = qimage2ndarray.array2qimage(self.GrayImg)
            #CVimg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
           
        else:
            CVimg = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        #print(CVimg.shape)       
            qimg = qimage2ndarray.array2qimage(CVimg)
        self.DispLb.setPixmap(QPixmap(qimg))
        self.DispLb.show()

    def CopyImg(self):
        ret=QRect(20,200,481,20)
        if self.GrayCheck.isChecked():
            qimg = qimage2ndarray.array2qimage(self.GrayImg)
            #CVimg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
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
        tag = self.RecordBt.text()
        if tag == 'Save Pic':
            image_name=self.RecordPath+'self.image'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.jpg'
            print(image_name)
            if self.GrayCheck.isChecked():
                cv2.imwrite(image_name,self.CVimg)
            else:
                cv2.imwrite(image_name,self.img)

            
        elif tag =='Record':
            self.RecordBt.setText('Stop')
            video_name = self.RecordPath + 'video' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.avi'
            if self.GrayCheck.isChecked():
                size = (self.GrayImg.shape[1],self.GrayImg.shape[0])
            else:
                size = (self.img.shape[1],self.img.shape[0])          
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            self.video_writer = cv2.VideoWriter(video_name, fourcc , self.camera.get(5), size)
            self.RecordFlag=1
            self.StopBt.setEnabled(False)
            self.ExitBt.setEnabled(False)

        elif tag == 'Stop':
            self.RecordBt.setText('Record')
            self.video_writer.release()
            self.RecordFlag = 0
            self.StopBt.setEnabled(True)
            self.ExitBt.setEnabled(True)


    def drawAvg(self):
        self.draw_2.clear()
        #inputImg= cv2.imread(self.img)
        #img = cv2.imread('rgb.png')
        img2RGB = cv2.cvtColor(self.img,cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img2RGB,cv2.COLOR_RGB2GRAY)
        #print(img2RGB.shape)
        #初始化numpy arr
        r_arr = np.zeros((640,1) , np.uint8)
        g_arr = np.zeros((640,1) , np.uint8)
        b_arr = np.zeros((640,1) , np.uint8)
        Gray_arr = np.zeros((640,1),np.uint8)
        for i in range(640):
            #print(np.sum(self.img[10:20 , i , 0] ))
            r_arr[i,0] = np.sum(img2RGB[220:240 , i , 0] )/ 20
            g_arr[i,0] = np.sum(img2RGB[220:240 , i , 1] )/ 20
            b_arr[i,0] = np.sum(img2RGB[220:240 , i , 2] )/ 20
            Gray_arr[i,0] = np.sum(gray[220:240 , i ])/ 20
            
        #rint(r_arr[0,0])

        x = np.linspace(0,640,640)
        self.draw_2.setRange(xRange=[0,640]) # 固定x軸 不會拉動
        self.draw_2.setRange(yRange=[0,255]) # 固定y軸 不會拉動
   
        self.draw_2.plot(x, r_arr[:,0] , pen='r')
        self.draw_2.plot(x, g_arr[:,0] , pen='g')
        self.draw_2.plot(x, b_arr[:,0] , pen='b')
        self.draw_2.plot(x,Gray_arr[:,0],pen='w')

    def calculate(self):
        pixel_array = []
        wave_array = []

        if self.P1.text():
            a1 = float(self.P1.text())
            pixel_array.append(a1)
            print("a1=",a1)
            if self.W1.text():
                b1 = float(self.W1.text())
                wave_array.append(b1)
                print("b1=",b1)

        if self.P2.text():
            a2 = float(self.P2.text())
            pixel_array.append(a2)
            
            if self.W2.text():
                b2 = float(self.W2.text())
                wave_array.append(b2)

        if self.P3.text():
            a3 = float(self.P3.text())
            pixel_array.append(a3)
            if self.W3.text():
                b3 = float(self.W3.text())
                wave_array.append(b3)

        if self.P4.text():
            a4 = float(self.P4.text())
            pixel_array.append(a4)
            if self.W4.text():
                b4 = float(self.W4.text())
                wave_array.append(b4)

        if self.P5.text():
             a5 = float(self.P5.text())
             pixel_array.append(a5)
             if self.W5.text():
                 b5 = float(self.W5.text())
                 wave_array.append(b5)  
        print(pixel_array)
        print(wave_array)

        """
        a1 = float(self.P1.text())
        a2 = float(self.P2.text())
        a3 = float(self.P3.text())
        a4 = float(self.P4.text())
        a5 = float(self.P5.text())
        """
        """ 
        b1 = float(self.W1.text())
        b2 = float(self.W2.text())
        b3 = float(self.W3.text())
        b4 = float(self.W4.text())
        b5 = float(self.W5.text())
        """
        x = pixel_array
        y = wave_array
        num = int(self.comboBox.currentText())
        parameter = np.polyfit(x,y,num)
        #parameter = np.polyfit(x,y,1)
        print(parameter)
        line = np.poly1d(parameter)
        print(line)
        #y2 = parameter[0] * x  + parameter[1]
        #print(y2)

        if num == 1:    
            result = "a1係數:"+ str(parameter[0]) + "\n" + "a0係數:"+ str(parameter[1]) +"\n"+ "y=" + str(line) 
            self.results_window.setText(result)
            self.graphicsView.plot(x,y,color='g')

        if num == 2:
            result = "a2係數:"+ str(parameter[0]) + "\n" + "a1係數:"+ str(parameter[1]) + "\n" + "a0係數:"+ str(parameter[2])  + "\n"+ "y=" + str(line)   
            self.results_window.setText(result)
            self.graphicsView.plot(x,y,color='g')

        if num == 3: 
            result = "a3係數:"+ str(parameter[0]) + "\n" +"a2係數:"+ str(parameter[1]) + "\n" + "a1係數:"+ str(parameter[2]) + "\n" + "a0係數:"+ str(parameter[3]) +"\n"+ "y=" + str(line)   
            self.results_window.setText(result)
            self.graphicsView.plot(x,y,color='g')

        if num == 4: 
            result = "a4係數:"+ str(parameter[0]) + "\n" +"a3係數:"+ str(parameter[1]) + "\n" + "a2係數:"+ str(parameter[2]) + "\n" + "a1係數:"+ str(parameter[3]) +"\n"+ "a0係數:"+ str(parameter[4]) + "\n"+ "y=" + str(line)   
            self.results_window.setText(result)
            self.graphicsView.plot(x,y,color='g')

        if num == 5: 
            result = "a5係數:"+ str(parameter[0]) + "\n" +"a4係數:"+ str(parameter[1]) + "\n" + "a3係數:"+ str(parameter[2]) + "\n" + "a2係數:"+ str(parameter[3]) +"\n"+ "a1係數:"+ str(parameter[4]) + "\n"+ "a0係數:"+ str(parameter[5]) +  "\n" + "y=" + str(line)   
            self.results_window.setText(result)
            self.graphicsView.plot(x,y,color='g')

    
       
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
