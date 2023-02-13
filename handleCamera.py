#!/usr/bin/env python3
# from asyncio.windows_events import NULL

import json
import time
import sys
import traceback
import numpy as np
import cv2
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer, CvSink
from networktables import NetworkTablesInstance
import aprilTagCap

configFile = "/boot/frc.json"


class CameraConfig: pass


team = None
server = True
cameraConfigs = []

print("stufferiiinos")

"""Report parse error."""


def parseError(str):
    print("config error in '" + configFile + "': " + str, file=sys.stderr)


"""Read single camera configuration."""


def readCameraConfig(config):
    cam = CameraConfig()

    # name
    try:
        cam.name = config["name"]
    except KeyError:
        parseError("could not read camera name")
        return False

    # path
    try:
        cam.path = config["path"]
    except KeyError:
        parseError("camera '{}': could not read path".format(cam.name))
        return False

    # stream properties
    cam.streamConfig = config.get("stream")

    cam.config = config

    cameraConfigs.append(cam)
    return True


"""Read configuration file."""


def readConfig():
    global team
    global server

    # parse file
    try:
        with open(configFile, "rt") as f:
            j = json.load(f)
    except OSError as err:
        print("could not open '{}': {}".format(configFile, err), file=sys.stderr)
        return False

    # top level must be an object
    if not isinstance(j, dict):
        parseError("must be JSON object")
        return False

    # team number
    try:
        team = j["team"]
    except KeyError:
        parseError("could not read team number")
        return False

    # ntmode (optional)
    if "ntmode" in j:
        str = j["ntmode"]
        if str.lower() == "client":
            server = False
        elif str.lower() == "server":
            server = True
        else:
            parseError("could not understand ntmode value '{}'".format(str))

    # cameras
    try:
        cameras = j["cameras"]
    except KeyError:
        parseError("could not read cameras")
        return False
    for camera in cameras:
        if not readCameraConfig(camera):
            return False

    return True


"""Start running the camera."""


def startCamera(config):
    print("Starting camera '{}' on {}".format(config.name, config.path))
    inst = CameraServer.getInstance()
    camera = UsbCamera(config.name, config.path)
    server = inst.startAutomaticCapture(camera=camera, return_server=True)

    camera.setConfigJson(json.dumps(config.config))
    camera.setConnectionStrategy(VideoSource.ConnectionStrategy.kKeepOpen)

    # this should be added to config not a default!!!!
    camera.setExposureManual(8)

    if config.streamConfig is not None:
        server.setConfigJson(json.dumps(config.streamConfig))

    return camera


def mainRun():
    # if __name__ == "__main__":
    # print(len(cameraConfigs))
    if len(sys.argv) >= 2:
        configFile = sys.argv[1]

    # read configuration
    if not readConfig():
        sys.exit(1)

    # start NetworkTables
    ntinst = NetworkTablesInstance.getDefault()
    ntinst.startClient(("10.8.30.2", 1735))

    table = ntinst.getTable("Shuffleboard")
    dashboard = table.getSubTable("vision")

    # start cameras
    cameras = []
    for cameraConfig in cameraConfigs:
        cameras.append(startCamera(cameraConfig))

    inst = CameraServer.getInstance()
    # following are default values from dashboard
    height = 120
    width = 160

    videoOutput = inst.putVideo("Camera Output", width, height)
    visionOutput = inst.putVideo("Vision Processed", width, height)
    videoSink = CvSink("Rasp PI Sink")

    frame = np.ndarray((height, width, 3))  # error
    lastfrontCamera = None
    dashboard.putNumber("Number of Cameras", len(cameras))

    dashboard.putNumber("tapeLowerH", 40)
    dashboard.putNumber("tapeLowerS", 150)
    dashboard.putNumber("tapeLowerV", 100)
    dashboard.putNumber("tapeUpperH", 80)
    dashboard.putNumber("tapeUpperS", 255)
    dashboard.putNumber("tapeUpperV", 255)

    # camera height in inches
    dashboard.putNumber("CameraHeight", 26)

    # camera angle in degrees
    dashboard.putNumber("CameraAngle", 33.92192950177638)

    # camera vertical FOV in degrees
    dashboard.putNumber("CameraVerticleFOV", 35)

    dashboard.putNumber("tapeToGapRatio", 0.93)

    # calibration distance from the edge of the hub to the camera in inches
    dashboard.putNumber("CalibrationDistance", 180)

    dashboard.putNumber("Hub Center X Distance", -1)

    dashboard.putNumber("Camera X Resolution", 1080)

    dashboard.putNumber("Zero if calibrate", 1)

    # vision processing
    while True:
        dashboard.putNumber("test", 101)
        # print("In the while")
        try:
            frontCamera = True

            # ("Line 158") # debugging
            if (frontCamera != lastfrontCamera):
                # print("Line 160") # debugging
                lastfrontCamera = frontCamera
                # print("Line 162") # debugging
                # print(lastfrontCamera)
                if (frontCamera):
                    # print('Set source 0 (front camera) (ball)')
                    videoSink.setSource(cameras[0])

            timeout = 0.225
            timestamp, frame = videoSink.grabFrame((120, 160, 3), timeout)  # this outputs a CvImage; IS ERROR
            if not timestamp:  # could not grab frame
                print("Frame skipped.")
                continue  # continue, just to ensure that we don't procsess empty frame
            # else:
            # print("frame not skipped")

            # *********************************
            # calls to vision Manipulation here, everything above handles vision hardwere configuration

            output = aprilTagCap.output(frame, dashboard)

            #output: 0. processed frame 1. number array whate




            videoOutput.putFrame(output[0])
            dashboard.putNumber("GAY", output[1])
        except Exception as e:
            print(e)
            print(traceback.format_exc())