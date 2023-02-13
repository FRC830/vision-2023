from aprilTagCap import AprilTagCap
from time import sleep
import cv2

a = AprilTagCap(0)

while True:
    a.display()
    a.show()
    cv2.imshow("OUT", a.frame)
