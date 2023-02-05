# imports
import apriltag
import cv2
import numpy as np
import time

#
# def processVideos(self, drawAxes=False, drawMask=False):
#     for atagcapture in self.apriltagcaptures:
#         if atagcapture.captureFrame() > 0 and atagcapture.genResults():
#             if drawAxes: atagcapture.drawAxes()
#             if drawMask: atagcapture.drawMask()
#             cameraname = atagcapture.getSink().getSource().getName()
#             cameratable = self.sd.getSubTable(cameraname)
#             translations, rotations, reprojerrors, timestamp, seenTagIDs = atagcapture.getTranslationsAngles(
#                 degrees=True)
#             self.tagIDs = 0 * self.tagIDs
#             for (tagID, translation, rotation, reprojerror) in zip(seenTagIDs, translations, rotations, reprojerrors):
#                 self.xTranslations[tagID] = translation[0]
#                 self.yTranslations[tagID] = translation[1]
#                 self.zTranslations[tagID] = translation[2]
#                 self.yawRotations[tagID] = rotation[0]
#                 self.confidences[tagID] = self.calculateConfidence(reprojerror)
#                 self.tagIDs[tagID] = 1
#
#             # Put Data into networktables
#             cameratable.putNumberArray("xTranslation", self.xTranslations)
#             cameratable.putNumberArray("yTranslation", self.yTranslations)
#             cameratable.putNumberArray("zTranslation", self.zTranslations)
#             cameratable.putNumberArray("yawRotation", self.yawRotations)
#             cameratable.putNumberArray("Confidence", self.confidences)
#             cameratable.putNumber("Timestamp", timestamp + self.timediff)
#             cameratable.putNumberArray("AprilTagIDs", seenTagIDs)

#
# params = {676.6192195641298, 676.8359339562655, 385.1137834870396, 201.81402152233636}



# Predefine variable

videoSource = 0

scale = 60

cap_fps = 1

prev_frame_time = 0

new_frame_time = 0

def setVar(source, scale):


# GENERAL

option = apriltag.DetectorOptions(families="tag16h5")

detector = apriltag.Detector(option)

source = cv2.VideoCapture(videoSource)

while cv2.waitKey(1) != 27:

    #
    # source.set(cv2.CAP_PROP_FPS, cap_fps)

    temp, image_old = source.read()
    if (temp == False):
        continue
    width = int(image_old.shape[1] * scale / 100)
    height = int(image_old.shape[0] * scale / 100)
    dim = (width, height)

    image = cv2.resize(image_old, dim, interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    gray = gray.astype(np.uint8)

    temp, binary = cv2.threshold(gray, 150, 230, cv2.THRESH_BINARY)

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
        # print(str(r.tag_id))
        # write a number
        cv2.putText(image, str(r.tag_id), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 2, cv2.LINE_4, False)

        # find Pos
        pose, a, b = detector.detection_pose(r, params)

        pose_new = {pose[0][3], pose[1][3], pose[2][3]}

        # print("FOLLOWING IS M")
        #print(type(pose))
        print("\r"+str(pose_new), end=" ")
        print("\t"+str(a)+"\t"+str(b), end=" ")
        # print(str)
        # print(str(r.corners))
        #print("FoLLOWING IS NOT M\n\n\n\n\n")
        #print(str(a))
        #print(str(b))

    cv2.imshow("OUT", image)
    # cv2.imshow("pre_processed", binary)

    time.sleep(0.5)

