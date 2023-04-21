import numpy as np 
import cv2

#load the image
image = cv2.imread("D:\screen1.png")

# grayscale
result = image.copy()
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray,100,200)
# adaptive threshold
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,53,7) 

# Fill rectangular contours
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #find only outside use RETR_EXTERNAL
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    if cv2.contourArea(c) > 1000:
        cv2.drawContours(thresh, [c], -1, (255,255,255), -1) #draw all contours pass -1;

# Morph open
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Draw rectangles, the 'area_treshold' value was determined empirically
# area_treshold = 1000
# for c in cnts:
#     if cv2.contourArea(c) > area_treshold :
#       x,y,w,h = cv2.boundingRect(c)
#       cv2.rectangle(image, (x, y), (x + w, y + h), (180,255,12), 2)

cv2.imshow('thresh', thresh)
cv2.imshow('opening', opening)
cv2.imwrite('sdf3.png',opening) #write (save)image;
# cv2.imshow('image', image)
cv2.waitKey()


img = cv2.imread("sdf3.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray,120,200)
contour,hierarchy = cv2.findContours(edge,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
drw = cv2.drawContours(img, contour, -1, (0,255,0), 2)
cv2.waitKey(0)
cv2.imshow('drw', drw)
cv2.waitKey()