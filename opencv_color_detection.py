#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Title: Opencv-color-detector
Description: Python script that allows you to detect a color in your webcam in real-time
Author: Daniel Verdu
Email: davertor@gmail.com
License: GNU
Version: 1.0.0
Date: 2018/08/13
'''


import numpy as np
import cv2
import argparse
from collections import deque


cap=cv2.VideoCapture(0)

pts = deque(maxlen=64)

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

while True:

	# Capture image from webcam
	ret, img=cap.read()

	# Change to HSV space. In HSV space is easier to find a color by only changing the hue
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	kernel=np.ones((5,5),np.uint8)

	# Applying a mask to the orig image to find desired object
	mask=cv2.inRange(hsv,lower_blue,upper_blue)
	mask = cv2.erode(mask, kernel, iterations=2)
	mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	#mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
	mask = cv2.dilate(mask, kernel, iterations=1)
	res=cv2.bitwise_and(img,img,mask=mask)

	# Find contours
	cnts,heir=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
	center = None
 
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		if radius > 5:
			cv2.circle(img, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(img, center, 5, (0, 0, 255), -1)
		
	pts.appendleft(center)

	for i in range(1,len(pts)):
		if pts[i-1]is None or pts[i] is None:
			continue
		thick = int(np.sqrt(len(pts) / float(i + 1)) * 2.5)
		cv2.line(img, pts[i-1],pts[i],(0,0,225),thick)
	
	cv2.imshow("Frame", img)
	cv2.imshow("mask",mask)
	cv2.imshow("res",res)
	
	k=cv2.waitKey(30) & 0xFF
	if k==32:
		break

# Cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()