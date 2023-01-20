# import the necessary packages\
import apriltag
import argparse
import cv2

import numpy as np

s = 0

source = cv2.VideoCapture(s)

win_name = 'Camera Preview'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)

while cv2.waitKey(1) != 27:  # Escape
    has_frame, image = source.read()

    img = image.astype(np.uint8)

    retval, binary = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

    results = detector.detect(binary)

    for r in results:
        (ptA, ptB, ptC, ptD) = r.corners
        ptA = (int(ptA[0]), int(ptA[1]))
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))

        cv2.line(image, ptA, ptB, (0, 255, 0), 2)

        cv2.line(image, ptB, ptC, (0, 255, 0), 2)

        cv2.line(image, ptC, ptD, (0, 255, 0), 2)

        cv2.line(image, ptD, ptA, (0, 255, 0), 2)

    # # extract the bounding box (x, y)-coordinates for the AprilTag
    # # and convert each of the (x, y)-coordinate pairs to integers
    # (ptA, ptB, ptC, ptD) = r.corners
    # ptB = (int(ptB[0]), int(ptB[1]))
    # ptC = (int(ptC[0]), int(ptC[1]))
    # ptD = (int(ptD[0]), int(ptD[1]))
    # ptA = (int(ptA[0]), int(ptA[1]))
    # # draw the bounding box of the AprilTag detection
    # cv2.line(image, ptA, ptB, (0, 255, 0), 2)
    # cv2.line(image, ptB, ptC, (0, 255, 0), 2)
    # cv2.line(image, ptC, ptD, (0, 255, 0), 2)
    # cv2.line(image, ptD, ptA, (0, 255, 0), 2)

    # (cX, cY) = (int(r.center[0]), int(r.center[1]))
    # cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

    if not has_frame:
        break
    cv2.imshow(win_name, frame)

source.release()
cv2.destroyWindow(win_name)






# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image containing AprilTag")
# args = vars(ap.parse_args())
# # load the input image and convert it to grayscale
# print("[INFO] loading image...")
# image = cv2.imread(args["image"])
# gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# image_NEW = gray.astype(np.uint8)

# retval, binary = cv2.threshold(image_NEW, 100, 255, cv2.THRESH_BINARY)


# # define the AprilTags detector options and then detect the AprilTags
# # in the input image
# print("[INFO] detecting AprilTags...")
# options = apriltag.DetectorOptions(families="tag36h11")
# detector = apriltag.Detector(options)
# results = detector.detect(binary)
# print("[INFO] {} total AprilTags detected".format(len(results)))


# # loop over the AprilTag detection results
# for r in results:
# 	# extract the bounding box (x, y)-coordinates for the AprilTag
# 	# and convert each of the (x, y)-coordinate pairs to integers
# 	(ptA, ptB, ptC, ptD) = r.corners
# 	ptB = (int(ptB[0]), int(ptB[1]))
# 	ptC = (int(ptC[0]), int(ptC[1]))
# 	ptD = (int(ptD[0]), int(ptD[1]))
# 	ptA = (int(ptA[0]), int(ptA[1]))
# 	# draw the bounding box of the AprilTag detection
# 	cv2.line(image, ptA, ptB, (0, 255, 0), 2)
# 	cv2.line(image, ptB, ptC, (0, 255, 0), 2)
# 	cv2.line(image, ptC, ptD, (0, 255, 0), 2)
# 	cv2.line(image, ptD, ptA, (0, 255, 0), 2)
# 	# draw the center (x, y)-coordinates of the AprilTag
# 	(cX, cY) = (int(r.center[0]), int(r.center[1]))
# 	cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
# 	# draw the tag family on the image
# 	tagFamily = r.tag_family.decode("utf-8")
# 	cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
# 		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
# 	print("[INFO] tag family: {}".format(tagFamily))


# # show the output image after AprilTag detection
# cv2.imshow("Image", image)
# cv2.waitKey(0)
