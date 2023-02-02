import pupil_apriltags
import cv2
import numpy as np


class AprilTagCap:
    def __init__(self, capture):
        self.stream = cv2.VideoCapture(capture)
        self.detector = pupil_apriltags.Detector()

    def getFrame(self):
        success, self.frame = self.stream.read()
        return success

    def processFrame(self):
        print(type(self.frame))
        print(self.frame)
        binary = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.image = cv2.threshold(binary, 150, 230, cv2.THRESH_BINARY)

    def getAprilTags(self):
        self.result = self.detector.detect(self.processFrame())

    def display(self):
        print(self.getFrame())
        self.processFrame()

    def show(self):
        cv2.imshow("OUT", self.frame)


