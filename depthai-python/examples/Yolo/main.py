#!/usr/bin/env python3

"""
The code is the same as for Tiny Yolo V3 and V4, the only difference is the blob file
- Tiny YOLOv3: https://github.com/david8862/keras-YOLOv3-model-set
- Tiny YOLOv4: https://github.com/TNTWEN/OpenVINO-YOLOV4
"""

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np
import time
import math
from VESC_instructions import VESC
from obs_avoid_2 import *
from VESC_instructions import VESC


def steering(x) -> float:
    # x represents the centroid's x position
    sv = (x - 0.5)/2.0 + 0.5
    # print(f'sv = {sv}')
    return sv

def throttle(width, scalar):
    # gas will be proportional to the width of the bounding box
    print(f"Bounding box width: {width}")
    if width < 0.6 and width > 0.1:
        #speed = 0.7*np.exp(0.21*(-width + 1)**5 + 2.0) - 5.06 # Extremely noticeable adaptive speed control
        speed = scalar*np.exp(-1.2*(width - 1.0)) - 0.04 #We want the speed to go down as the width gets larger
        
    else: 
        speed = 0
    print(f"Speed: {speed}") 
    return speed

# nn data, being the bounding box locations, are in <0..1> range - they need to be normalized with frame width/height
def frameNorm(frame, bbox):
    normVals = np.full(len(bbox), frame.shape[0])
    normVals[::2] = frame.shape[1]
    return (np.clip(np.array(bbox), 0, 1) * normVals).astype(int)

def displayFrame(name, frame) -> list:
    color = (255, 0, 0)
    # Center variable will have the following elements: [centerX, centerY, BBwidth]
    center = [0, 0, 0]
    for detection in detections:
        if detection.label == 0:
            bbox   = frameNorm(frame, (detection.xmin, detection.ymin, detection.xmax, detection.ymax))
            width  = float(abs(detection.xmax - detection.xmin))
            height = float(abs(detection.ymax - detection.ymin))

            center[0] = (float(detection.xmin) + width/2.0)
            center[1] = (float(detection.ymin) + height/2.0)
            center[2] = width
            #cv2.putText(frame, labelMap[detection.label], (bbox[0] + 10, bbox[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            #cv2.putText(frame, f"{int(detection.confidence * 100)}%", (bbox[0] + 10, bbox[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            #cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            break
    return center

# Create a VESC object
VESC_module = VESC('/dev/ttyACM0')


# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
depth = pipeline.create(dai.node.StereoDepth)
xout = pipeline.create(dai.node.XLinkOut)

xout.setStreamName("disparity")

# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)

# Linking
monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)
depth.disparity.link(xout.input)














# Get argument first
nnPath = str((Path(__file__).parent / Path('../models/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
if 1 < len(sys.argv):
    arg = sys.argv[1]
    if arg == "yolo3":
        nnPath = str((Path(__file__).parent / Path('../models/yolo-v3-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
    elif arg == "yolo4":
        nnPath = str((Path(__file__).parent / Path('../models/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
    else:
        nnPath = arg
else:
    print("Using Tiny YoloV4 model. If you wish to use Tiny YOLOv3, call 'tiny_yolo.py yolo3'")

if not Path(nnPath).exists():
    import sys
    raise FileNotFoundError(f'Required file/s not found, please run "{sys.executable} install_requirements.py"')

# tiny yolo v4 label texts
labelMap = [
    "person",         "bicycle",    "car",           "motorbike",     "aeroplane",   "bus",           "train",
    "truck",          "boat",       "traffic light", "fire hydrant",  "stop sign",   "parking meter", "bench",
    "bird",           "cat",        "dog",           "horse",         "sheep",       "cow",           "elephant",
    "bear",           "zebra",      "giraffe",       "backpack",      "umbrella",    "handbag",       "tie",
    "suitcase",       "frisbee",    "skis",          "snowboard",     "sports ball", "kite",          "baseball bat",
    "baseball glove", "skateboard", "surfboard",     "tennis racket", "bottle",      "wine glass",    "cup",
    "fork",           "knife",      "spoon",         "bowl",          "banana",      "apple",         "sandwich",
    "orange",         "broccoli",   "carrot",        "hot dog",       "pizza",       "donut",         "cake",
    "chair",          "sofa",       "pottedplant",   "bed",           "diningtable", "toilet",        "tvmonitor",
    "laptop",         "mouse",      "remote",        "keyboard",      "cell phone",  "microwave",     "oven",
    "toaster",        "sink",       "refrigerator",  "book",          "clock",       "vase",          "scissors",
    "teddy bear",     "hair drier", "toothbrush"
]

syncNN = True

# Define sources and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
detectionNetwork = pipeline.create(dai.node.YoloDetectionNetwork)
xoutRgb = pipeline.create(dai.node.XLinkOut)
nnOut = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")
nnOut.setStreamName("nn")

# Properties
camRgb.setPreviewSize(416, 416)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
camRgb.setFps(40)

# Network specific settings
detectionNetwork.setConfidenceThreshold(0.5)
detectionNetwork.setNumClasses(80)
detectionNetwork.setCoordinateSize(4)
detectionNetwork.setAnchors([10, 14, 23, 27, 37, 58, 81, 82, 135, 169, 344, 319])
detectionNetwork.setAnchorMasks({"side26": [1, 2, 3], "side13": [3, 4, 5]})
detectionNetwork.setIouThreshold(0.5)
detectionNetwork.setBlobPath(nnPath)
detectionNetwork.setNumInferenceThreads(2)
detectionNetwork.input.setBlocking(False)

# Linking
camRgb.preview.link(detectionNetwork.input)
if syncNN:
    detectionNetwork.passthrough.link(xoutRgb.input)
else:
    camRgb.preview.link(xoutRgb.input)

detectionNetwork.out.link(nnOut.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queues will be used to get the rgb frames and nn data from the outputs defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    qDet = device.getOutputQueue(name="nn", maxSize=4, blocking=False)

    q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)

    priority = False
    count = 0
    sv_avg = 0.0
    while True:
        try:
            inDisparity = q.get()  # blocking call, will wait until a new data has arrived
        except RuntimeError:
                print("RuntimeError detected! (1)")
                continue
        frame = inDisparity.getFrame()
        frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
        bucket, turn_dir, avg_depth = quadrents(5,frame[:,0:550],0.75)
        throttle_value = 0
        if avg_depth > 50:
            turn_input = turn_dir  # If our depth is above the threshold, set the variable == output of function
            priority = True            
        else:
            turn_input = 0.5 # Center the wheels
            priority = False

        #print(priority)
        frame = None
        detections = []
        startTime = time.monotonic()
        counter = 0
        color2 = (255, 255, 255)

        if syncNN:
            try:
                inRgb = qRgb.get()
                inDet = qDet.get()
            except RuntimeError:
                print("RuntimeError detected! (1)")
                continue
        else:
            try:
                inRgb = qRgb.tryGet()
                inDet = qDet.tryGet()
            except RuntimeError:
                print("RuntimeError detected! (2)")
                continue

        if inRgb is not None:
            frame = inRgb.getCvFrame()
            cv2.putText(frame, "NN fps: {:.2f}".format(counter / (time.monotonic() - startTime)),
                        (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color2)

        if inDet is not None:
            detections = inDet.detections
            counter += 1

        if frame is not None:
            center = displayFrame("rgb", frame)
            centerX = center[0]
            width = center[2]
            sv = steering(centerX)
            if count != 5:
                sv_avg = sv_avg + sv
                count = count + 1
            else:
                count = 0
                sv_avg = sv_avg/5.0
                speed = throttle(width,0.08) 
                if priority == False:
                    if speed == 0:
                        print("Human lost or too close!")
                        VESC_module.run(turn_input, speed)
                    else:
                        VESC_module.run(sv_avg, speed) 
                    print("\nFollowing!\n")
                else:
                    VESC_module.run(turn_input, speed) 
                    print("\nAvoiding!\n")

                sv_avg = 0.0
            time.sleep(0.01)
