import cv2
import apriltag
import numpy as np

image = cv2.imread("aprilTag4.jpg")

scale_percent = 60  # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
def resizeImage(scale_percent, image):
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def proccessImage(resized):
    gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)

    image_NEW = gray.astype(np.uint8)

    retval, binary = cv2.threshold(image_NEW, 100, 255, cv2.THRESH_BINARY)

    return binary

# define the AprilTags detector options and then detect the AprilTags
# in the input image
def detectAprilTags(binary):
    print("[INFO] detecting AprilTags...")
    options = apriltag.DetectorOptions(families="tag16h5")
    detector = apriltag.Detector(options)
    results = detector.detect(binary)
    print("[INFO] {} total AprilTags detected".format(len(results)))

    cv2.imshow("Bin", binary)

    print(results)
    return results



# loop over the AprilTag detection results
def loopResults(resized, results):
    for r in results:
        # extract the bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))
        # draw the bounding box of the AprilTag detection
        cv2.line(resized, ptA, ptB, (0, 255, 0), 2)
        cv2.line(resized, ptB, ptC, (0, 255, 0), 2)
        cv2.line(resized, ptC, ptD, (0, 255, 0), 2)
        cv2.line(resized, ptD, ptA, (0, 255, 0), 2)
        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(resized, (cX, cY), 5, (0, 0, 255), -1)
        # draw the tag family on the image
        tagFamily = r.tag_family.decode("utf-8")
        cv2.putText(resized, tagFamily, (ptA[0], ptA[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print("[INFO] tag family: {}".format(tagFamily))

# show the output image after AprilTag detection
def displayOutputImage(resized):
    cv2.imshow("Image", resized)
    cv2.waitKey(0)