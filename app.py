from Ui_Pixel2Wave import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
from PyQt5.QtCore import QTimer,QCoreApplication
from PyQt5.QtGui import QPixmap
import cv2
import qimage2ndarray
import pyqtgraph as py
import numpy as np
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import Qt,QRect
import matplotlib.pyplot as plt
import pyqtgraph as pg 

class CurveFitting(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
         super(CurveFitting,self).__init__(parent)
         self.setupUi(self)
         self.BtnGo.clicked.connect(self.calculate)
         

    def calculate(self):
        a1 = float(self.P1.toPlainText())
        a2 = float(self.P2.toPlainText())
        a3 = float(self.P3.toPlainText())
        a4 = float(self.P4.toPlainText())
        #a5 = float(self.P5.toPlainText())

        b1 = float(self.W1.toPlainText())
        b2 = float(self.W2.toPlainText())
        b3 = float(self.W3.toPlainText())
        b4 = float(self.W4.toPlainText())
        #b5 = float(self.W5.toPlainText())
        
        x = np.array([a1,a2,a3,a4])
        y = np.array([b1,b2,b3,b4])
        parameter = np.polyfit(x,y,1)
        print(parameter)
        line = np.poly1d(parameter)
        print(line)
        y2 = parameter[0] * x  + parameter[1]
        print(y2)

        result = "a1係數:"+ str(parameter[0]) + "\n" + "a0係數:"+ str(parameter[1]) +"\n"+ "y=" + str(line)        
        self.results_window.setText(result)

        self.graphicsView.plot(x,y2, pen='g', hold=False)
       




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui=CurveFitting()
    ui.show()
    app.exec_()
    
