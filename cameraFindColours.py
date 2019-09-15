import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import imutils
import explorerhat
from time import sleep

import board
import neopixel

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(0.1)
 
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# define the list of boundaries
boundaries = [
	("red", [5, 0, 58], [45, 39, 98]),
	("purple", [235, 93, 92], [255, 133, 122]),	
	("blue", [235, 209, 133], [255, 249, 173]),
	("green", [79, 125, 71], [119, 155, 111])
]

# loop through the colours
for i, (colorname, lower, upper) in enumerate(boundaries):

	print("Question: Does it have "+colorname+"?")
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
 
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	
	#get rid of blobs	
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
		
	output = cv2.bitwise_and(image, image, mask = mask)
	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	
	if len(cnts) > 0:
	
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)	
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))	
		
		if radius > 10:
			cv2.circle(output, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv2.circle(output, center, 5, (0, 0, 255), -1)
			print ("Answer: Yes")
		else:
			print ("Answer: No")
	else:
		print ("Answer: No")
		
	
	#show image side by side
	cv2.imwrite("i%d.jpg" %i, np.hstack([image, output]))
	cv2.imwrite(colorname+".jpg", output)
	#cv2.waitKey(0)
	