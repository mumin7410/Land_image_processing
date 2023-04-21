import cv2 
import numbers as np
from PIL import Image
##กันลืม if find marker the zoom in to marker: like zoom in to face ig filter;
img = cv2.imread("D:\screen2.png")
cv2.rectangle(img, (290,150),(620,400),(0,255,0),3)
roi = img[150:400,290:620]
cv2.imshow('image',roi)
cv2.waitKey(0)
# cv2.imshow('image',img2)
# cv2.waitKey(0)

