import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
imgSize = 300
counter = 0
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

folder = "Data/Thumb"

labels = ["Thumb", "OK", "Left"]


class handSign():
    def imgProcess(self, img, hands, imgSize):
        global imgWhite
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # matrix of ones
            imgCrop = img[y - 20:y + h + 20, x - 20:x + w + 20]
            imgCropShape = imgCrop.shape
            imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop
        return imgWhite

    def handSignDetect(self, imgWhite):
        prediction, index = classifier.getPrediction(imgWhite)
        return index

def main():
    while True:
        sucesss, img = cap.read()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # matrix of ones
            imgCrop = img[y - 20:y + h + 20, x - 20:x + w + 20]

            imgCropShape = imgCrop.shape

            imgWhite[0:imgCropShape[0], 0:imgCropShape[1]] = imgCrop
            prediction, index = classifier.getPrediction(imgWhite)
            print(index)
            cv2.imshow("White", imgWhite)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()