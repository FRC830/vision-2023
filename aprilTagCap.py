import pupil_apriltags
import cv2
import numpy as np
import time


class AprilTagCap:
    def __init__(self, capture, scale, fps, prev_frame_time, new_frame_time):
        self.stream = cv2.VideoCapture(capture)
        self.detector = pupil_apriltags.Detector()
        self.scale = scale
        self.fps = fps
        self.prev_frame_time = prev_frame_time
        self.new_frame_time = new_frame_time

  
    def Scale(img, source, scale, detector):
        while cv2.waitKey(1) != 27:
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
        
        return binary

    def getFrame(image):
         # FPS
        new_frame_time = time.time()

        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        cv2.putText(image, str(int(fps)), (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4, False)

    def proccessing(image, results, detector):
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


