import cv2
import numpy as np
import pyqtgraph as pg

img = cv2.imread('rgb.png')
img2RGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#print(img2RGB)
#print(img2RGB.shape)

#print(np.sum(img2RGB[200:300, 0, 0]) / 100)
r_arr = np.zeros((500,1) , np.float16)
g_arr = np.zeros((500,1) , np.float16)
b_arr = np.zeros((500,1) , np.float16)
for i in range(500):
    r_arr[i,0] = np.sum(img2RGB[10:20 , i , 0] / 10)
    g_arr[i,0] = np.sum(img2RGB[10:20 , i , 1] / 10)
    b_arr[i,0] = np.sum(img2RGB[10:20 , i , 2] / 10)
    print('R: ' , r_arr[i,0])
    print('G: ' , g_arr[i,0])
    print('B: ' , b_arr[i,0])

app = pg.mkQApp()
plot = pg.plot(title='Rainbow')
x = np.linspace(0,500,500)
plot.plot(x, r_arr[:,0] , pen='r')
plot.plot(x, g_arr[:,0] , pen='g')
plot.plot(x, b_arr[:,0] , pen='b')


app.exec_() 




