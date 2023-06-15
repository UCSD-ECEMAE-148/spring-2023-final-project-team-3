#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np
# from obs_avoid_2 import quadrents, turn_value
from obs_avoid_2 import *
from VESC_instructions import VESC

# Create VESC object
VESC_module = VESC('/dev/ttyACM1')
# Example command
# VESC_module.run(0,0.2)


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


# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the disparity frames from the outputs defined above
    q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
    #print("test")
    #throttle_value = 0.15
    priority = False
    while True:

      inDisparity = q.get()  # blocking call, will wait until a new data has arrived
      frame = inDisparity.getFrame()
      # Normalization for better visualization
      frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
      # print(frame,type(frame))
      # print(np.shape(frame))
      #cv2.imshow("disparity", frame)
      #cv2.waitKey(1)
      # np.savetxt('my_array.txt', frame)
      bucket, turn_dir, avg_depth = quadrents(5,frame[:,0:550],0.75)
      #print("Avg depth",avg_depth)
      throttle_value = 0
      if avg_depth > 50:
        turn_input = turn_dir  # If our depth is above the threshold, set the variable == output of function
        #print(turn_input)
        priority = True
        VESC_module.run(turn_input, throttle_value)
      else:
        turn_input = 0.5 #Center the wheels
        #print(turn_input)
        priority = False
        #VESC_module.run(turn_input, throttle_value)
      '''
        if priority == False:
        else:
          VESC_module.run(turn_input, throttle_value)
      '''
        # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html

        #frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
       
        #cv2.imshow("disparity", frame[:,0:550])
        #cv2.waitKey(1)
       






        # cv2.imshow("disparity_color", frame)

        # if cv2.waitKey(1) == ord('q'):
        #     break
