import cv2
import numpy as np

image = cv2.imread("D:\screen1.png")

#grayScale:
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray,100,200)

#find contour:

cv2.imshow('test',edge)
cv2.waitKey(0)