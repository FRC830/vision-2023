# imports
import apriltag
import cv2
import numpy as np
import time

# Predefine variable

videoSource = 0

scale = 60

cap_fps = 30

prev_frame_time = 0

new_frame_time = 0

# GENERAL

option = apriltag.DetectorOptions(families="tag16h5")

detector = apriltag.Detector(option)

source = cv2.VideoCapture(videoSource)

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

    text = "aprilTag num:\t{a}".format(a=len(results))

    cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4, False)

    # FPS
    new_frame_time = time.time()

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time

    cv2.putText(image, str(int(fps)), (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4, False)

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
        # new code
        # find distance
        print(str(r.tag_id))
        # write a number
        cv2.putText(image, str(r.tag_id), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 255, 0), 2, cv2.LINE_4, False)
        
    
    cv2.imshow("OUT", image)
    