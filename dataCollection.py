import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
imgSize = 300
counter = 0
folder = "Data/Left"
while True:
    sucesss, img = cap.read()
    hands,img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x,y,w,h = hand['bbox']
        imgWhite = np.ones((imgSize, imgSize,3),np.uint8)*255 #matrix of ones
        imgCrop = img[y-20:y+h+20,x-20:x+w+20]

        imgCropShape = imgCrop.shape

        imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop
        cv2.imshow("Crop", imgCrop)
        cv2.imshow("White", imgWhite)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg',imgWhite)
        print(counter)

cv2.release()
cv2.destroyAllWindows()