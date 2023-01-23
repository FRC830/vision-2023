# import the necessary packages\
import apriltag
import argparse
import cv2

import numpy as np

videoinput = 0

scale_percent = 60  # percent of original size

source = cv2.VideoCapture(videoinput)

while cv2.waitKey(1) != 27:  # Escape
    has_frame, image_og = source.read()

    width = int(image_og.shape[1] * scale_percent / 100)
    height = int(image_og.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(image_og, dim, interpolation=cv2.INTER_AREA)

    img = resized.astype(np.uint8)

    image_NEW = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    retval, binary = cv2.threshold(image_NEW, 100, 255, cv2.THRESH_BINARY)

    options = apriltag.DetectorOptions(families="tag36h11")

    detector = apriltag.Detector(options)

    results = detector.detect(image_NEW)

    print("[INFO] {} total AprilTags detected".format(len(results)))

    for r in results:
        (ptA, ptB, ptC, ptD) = r.corners

        ptA = (int(ptA[0]), int(ptA[1]))
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))

        print(ptA)
        print(ptB)
        print(ptC)
        print(ptD)

        cv2.line(img, ptA, ptB, (0, 255, 0), 2)

        cv2.line(img, ptB, ptC, (0, 255, 0), 2)

        cv2.line(img, ptC, ptD, (0, 255, 0), 2)

        cv2.line(img, ptD, ptA, (0, 255, 0), 2)

    if not has_frame:
        break
    cv2.imshow("OUT", img)
    cv2.imshow("Binary", binary)

source.release()
cv2.destroyWindow(win_name)
