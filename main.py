#imports
import apriltag
import cv2
import numpy as np


#Predefine variable

videoSource = 0

scale = 60

source = cv2.VideoCapture(videoSource)

#APRILTAG SECTION

option = apriltag.DetectorOptions(families="tag16h5")

detector = apriltag.Detector(option)


while cv2.waitKey(1) != 27:
    temp, image_old = source.read()

    width = int(image_old.shape[1] * scale / 100)
    height = int(image_old.shape[0] * scale / 100)
    dim = (width, height)

    image = cv2.resize(image_old, dim, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    gray = gray.astype(np.uint8)

    temp, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    results = detector.detect(binary)

    for r in results:
        # extract R bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))
        # draw the bounding box of the AprilTag detection
        cv2.line(image, ptA, ptB, (0, 255, 0), 2)
        cv2.line(image, ptB, ptC, (0, 255, 0), 2)
        cv2.line(image, ptC, ptD, (0, 255, 0), 2)
        cv2.line(image, ptD, ptA, (0, 255, 0), 2)
        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
        # draw the tag family on the image
        tagFamily = r.tag_family.decode("utf-8")
        cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print("[INFO] tag family: {}".format(tagFamily))

    cv2.imshow("OUT", image)