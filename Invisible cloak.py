# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 13:01:12 2020

@author: ACER
"""


import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
cnt =0
backgrnd =0

for i in range(60):                 #capturing the empty frame forbackground in a range(60)
    ret,backgrnd = cap.read()
    if ret==False:
        continue
#print(backgrnd)
backgrnd = np.flip(backgrnd,axis=1)

while cap.isOpened():
    ret1,img = cap.read()
    if ret1==False:
        break
    cnt+=1                        #To count num of frames
    img = np.flip(img, axis = 1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_red = np.array([100, 40, 40])	 
    upper_red = np.array([100, 255, 255])
    mask1 = cv2.inRange(hsv,lower_red,upper_red)                        #It is a binary image so returns a pixel of value 1(white) if it is in range else returns 0(black)
    lower_red = np.array([155, 40, 40]) 
    upper_red = np.array([180, 255, 255]) 
    mask2 = cv2.inRange(hsv, lower_red, upper_red)          
    #cv2.imshow("Mask2",mask2)    #Red objects become white
    #cv2.imshow("Mask1",mask1)    #Red objects become black
    mask1 = mask1+mask2
    #cv2.imshow("New",mask1)       #Become white
    kernel=np.ones((5,5),np.uint8)
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,kernel,iterations=2)   #Erosion followed by dilation takes place here which is called as opening
    mask1 = cv2.dilate(mask1,kernel,iterations=1)
    mask2=cv2.bitwise_not(mask1)                                         #bitwise_not changes backgrnd to foregrnd i.e it reverses both back and foregrnd.
    res1 = cv2.bitwise_and(backgrnd, backgrnd, mask = mask1 )    
    res2 = cv2.bitwise_and(img, img, mask = mask2) 
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 
    #cv2.imshow("hjg",backgrnd)   
    #cv2.imshow("IMg",img)
    #cv2.imshow("res1",res1)
    #cv2.imshow("res2",res2)
    cv2.imshow("INVISIBLE MAN", final_output)
    k = cv2.waitKey(10)
    if k==27:
        break
    
cap.release()
#cv2.imshow("First mask",mask1)  #Full black window
#cv2.imshow("bitwise not",mask2)  #Full white window
#cv2.waitKey(0) 
cv2.destroyAllWindows()
print("No.of frames recorded",cnt)
