import cv2
import mediapipe as mp
import time
import handSignModule as hsm
import System as stm
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import handTrackingMod as htm
import keyboard
import math
detectorSign = hsm.handSign()
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
detectorMod = htm.handDetector()
imgSize = 300
tipIds = [4, 8, 12, 16, 20]
tempIndx = 10
def fingerCount(img):
    tipIds = [4,8,12,16,20]
    img = detectorMod.findHands(img)
    lmList = detectorMod.findPosition(img, draw=False)
    fingersCount = 0
    if len(lmList) != 0:
        fingersState = []
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingersState.append(1)
        else:
            fingersState.append(0)
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingersState.append(1)
            else:
                fingersState.append(0)
        fingersCount = fingersState.count(1)

    return fingersCount

def fingerDetect(img, hands):
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # matrix of ones
        imgCrop = img[y - 20:y + h + 20, x - 20:x + w + 20]
        imgCropShape = imgCrop.shape
        imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop


    return imgWhite

while not keyboard.is_pressed("s"):
    success, img = cap.read()
    img = detectorMod.findHands(img)
    cv2.putText(img, "Raise your hand sign and press S", (45, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)

cv2.destroyAllWindows()

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    key = "NULL"
    left = "NULL"
    index = 2
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # matrix of ones
        imgCrop = img[y - 20:y + h + 20, x - 20:x + w + 20]
        imgCropShape = imgCrop.shape
        imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop
        index = detectorSign.handSignDetect(imgWhite)
        cv2.imshow("White", imgWhite)
        tempIndx = index

    if tempIndx == 0:
        while not keyboard.is_pressed("s"):
            success, img = cap.read()
            img = detectorMod.findHands(img)
            lmList = detectorMod.findPosition(img, draw=False)
            fingersCount = 0
            if len(lmList) != 0:
                fingersState = []
                if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                    fingersState.append(1)
                else:
                    fingersState.append(0)
                for id in range(1, 5):
                    if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                        fingersState.append(1)
                    else:
                        fingersState.append(0)
                fingersCount = fingersState.count(1)
                stm.countLed(fingersCount)
            success, img = cap.read()
            hand, img = detector.findHands(img)
            imgWhite = fingerDetect(img, hands)
            tempIndx = detectorSign.handSignDetect(imgWhite)
            cv2.putText(img, "COUNTING", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 10)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        cv2.putText(img, "TRACKING!", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 10)
        cv2.putText(img, "Leave S to stop TRACKING", (45, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    if tempIndx == 1:
        while not keyboard.is_pressed("s"):
            print("OKsign")
            success, img = cap.read()
            img = detectorMod.findHands(img)
            lmList = detectorMod.findPosition(img, draw=False)
            if len(lmList) != 0:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx,cy = (x1+x2)//2, (y1+y2)//2
                cv2.circle(img,(x1,y1),12,(255,0,255),cv2.FILLED)
                cv2.circle(img, (x2, y2), 12, (255, 0, 255), cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)

                length = math.hypot(x2-x1, y2-y1)
                stm.adjustBright(length)
            imgWhite = fingerDetect(img, hands)
            tempIndx = detectorSign.handSignDetect(imgWhite)
            cv2.putText(img, "ADJUST", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 10)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        cv2.putText(img, "TRACKING!", (45,375), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 10)
        cv2.putText(img, "Leave S to stop TRACKING", (45, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        # if index == 2:
        #     if index == 1:
        #         while not :
        #             print(fingerCount(img, index))

        #print(indexFinger[index])
    cv2.imshow("Image", img)
    cv2.waitKey(1)
