import pupil_apriltags
import cv2
import numpy as np


class AprilTagCap:
    def __init__(capture):
        self.stream = cv2.VideoCapture(capture)

