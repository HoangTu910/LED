import cv2
import mediapipe as mp
import time
import handTrackingMod as htm

cap = cv2.VideoCapture(0)
detector = htm.handDetector()
tipIds = [4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingersState = []
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingersState.append(1)
        else:
            fingersState.append(0)
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingersState.append(1)
            else:
                fingersState.append(0)
        fingerCount = fingersState.count(1)
        print(fingerCount)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()

