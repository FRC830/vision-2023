# imports
import apriltag
import cv2
import numpy as np
import math
import time


def list_ports():
    """
    Test the ports and returns a tuple with the available ports 
    and the ones that are working.
    """
    is_working = True
    dev_port = 0
    working_ports = []
    available_ports = []
    while is_working:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports

def processVideos(self, drawAxes=False, drawMask=False):
    for atagcapture in self.apriltagcaptures:
        if atagcapture.captureFrame() > 0 and atagcapture.genResults():
            if drawAxes: atagcapture.drawAxes()
            if drawMask: atagcapture.drawMask()
            cameraname = atagcapture.getSink().getSource().getName()
            cameratable = self.sd.getSubTable(cameraname)
            translations, rotations, reprojerrors, timestamp, seenTagIDs = atagcapture.getTranslationsAngles(
                degrees=True)
            self.tagIDs = 0 * self.tagIDs
            for (tagID, translation, rotation, reprojerror) in zip(seenTagIDs, translations, rotations, reprojerrors):
                self.xTranslations[tagID] = translation[0]
                self.yTranslations[tagID] = translation[1]
                self.zTranslations[tagID] = translation[2]
                self.yawRotations[tagID] = rotation[0]
                self.confidences[tagID] = self.calculateConfidence(reprojerror)
                self.tagIDs[tagID] = 1

            # Put Data into networktables
            cameratable.putNumberArray("xTranslation", self.xTranslations)
            cameratable.putNumberArray("yTranslation", self.yTranslations)
            cameratable.putNumberArray("zTranslation", self.zTranslations)
            cameratable.putNumberArray("yawRotation", self.yawRotations)
            cameratable.putNumberArray("Confidence", self.confidences)
            cameratable.putNumber("Timestamp", timestamp + self.timediff)
            cameratable.putNumberArray("AprilTagIDs", seenTagIDs)


params = {678.154, 678.17, 318.135, 228.374}



# Predefine variable
list_ports()

videoSource = 1

scale = 60

cap_fps = 1

prev_frame_time = 0

new_frame_time = 0

# GENERAL

option = apriltag.DetectorOptions(families="tag36h11")

detector = apriltag.Detector(option)

source = cv2.VideoCapture(videoSource)

while cv2.waitKey(1) != 27:



    #
    # source.set(cv2.CAP_PROP_FPS, cap_fps)

    temp, image_old = source.read()
    if (temp == False):
        continue
    # width = int(image_old.shape[1] * scale / 100)
    # height = int(image_old.shape[0] * scale / 100)
    dim = (640, 480)

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

        # find Pos
        pose, a, b = detector.detection_pose(r, params)

        pose_new = [pose[0][3], pose[1][3], pose[2][3]]
        temp = pose_new.copy()

        # print("FOLLOWING IS M")
        #print(type(pose))

        # for i in pose: 
        #     print(str(i))

        # print("\r"+str(pose_new), end=" ")
        x = pose_new[0]
        y = pose_new[2]
        print("\tx:"+str(x)+"\t z:"+str(y)+"\t hyp"+str(math.sqrt(pow(x, 2) + pow(y, 2))),flush=True  )
        
        
        # print(str)
        # print(str(r.corners))
        #print("FoLLOWING IS NOT M\n\n\n\n\n")
        #print(str(a))
        #print(str(b))

    cv2.imshow("OUT", image)
    # cv2.imshow("pre_processed", binary)

    # time.sleep(0.5)


    print("FOLLOWING IS M")
    print(str(pose))
    print(str(r.corners))
    print("FoLLOWING IS NOT M\n\n\n\n\n")
    print(str(a))
    print(str(b))

    cv2.imshow("OUT", image)
