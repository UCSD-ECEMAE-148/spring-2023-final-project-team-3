#!/usr/bin/env python3
# coding: utf-8

import cv2
import depthai as dai
import numpy as np
from VESC_instructions import VESC

'''Creating an instance of VESC class using the serial port parameter'''

VESC_module = VESC('/dev/ttyACM0')

while True:
	print('Controls: wasd')
	user = input()
	if (user=='w'): # Forward
		VESC_module.run(0,0.2)
	elif (user=='a'): # Left
		VESC_module.run(-1,0)
	elif (user=='s'): # Backward
		VESC_module.run(0,-0.2)
	elif (user=='d'): # Right
		VESC_module.run(1,0)
