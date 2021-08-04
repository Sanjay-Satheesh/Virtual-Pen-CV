import cv2
import numpy as np
import time
import os
import TrackHandMod as thm

bThick = 15



cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4, 720)

detectorH = thm.HDetector(detectionCon=0.85)
x0, y0 = 0, 0
imgBoard = np.zeros((720, 1280, 3), np.uint8)
dColor = (255,0,255)
while True:
    success, img = cap.read()
    
    img = cv2.flip(img, 1)
    img = detectorH.findH(img)
    HList = detectorH.findPos(img, draw=False)
    

    if len(HList) != 0:
        #print(lmList)

        #tip of index and middle finger 
        x1, y1 = HList[8][1:]
        x2, y2 = HList[12][1:]
        x3, y3 = HList[20][1:]
        FList = detectorH.fingerCheck()
        #print(fingers)

        if FList[1] and FList[2]:
            cv2.rectangle(img, (x1, y1-25), (x2,y2+25), dColor, cv2.FILLED)
            print("selection Mode") 
            x0, y0 = 0, 0

        if FList[1] and FList[2]==False:
            cv2.circle(img, (x1,y1), 15, dColor, cv2.FILLED)
            print("Drawing Mode")
            if x0==0 and y0==0:
                x0,y0 = x1,y1

            cv2.line(img, (x0,y0), (x1,y1), dColor, bThick)
            cv2.line(imgBoard, (x0,y0), (x1,y1), dColor, bThick)


            x0,y0 = x1,y1
        if FList[3] and FList[4]:
            cv2.rectangle(img, (x1, y1-25), (x3,y3+25), (0,0,0), cv2.FILLED)
            if x0==0 and y0==0:
                x0, y0 = x1,y1
            
            cv2.line(imgBoard, (x0,y0), (x1,y1), (0,0,0), 50)
            x0,y0 = x1, y1

    imgNew = cv2.cvtColor(imgBoard, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgNew, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.THRESH_BINARY_INV)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgBoard)



    img = cv2.addWeighted(img, 0.5, imgBoard, 0.5,0)
    cv2.imshow("Image", img)
    #cv2.imshow("Drawing Board", imgBoard)
    cv2.waitKey(1)

    