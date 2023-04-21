from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
import time
from PIL import Image
import pandas as pd
import cv2 

#initial:
PATH = "D:\chromedriver.exe" ##google driver PATH;
driver = webdriver.Chrome(PATH)
driver.get("https://landsmaps.dol.go.th")
arr = []

#delete first popup
# time.sleep(2)
# out = driver.find_element(By.XPATH,"//div[@id='modal_news']/div/div/div/button").click()

#!!!delay for 10 seconds.
time.sleep(10)
#!!click view tab;
driver.find_element(By.ID,"layer").click()
time.sleep(2)
driver.find_element(By.ID,"GoogleMap").click()
time.sleep(2)
#!!close view tab
driver.find_element(By.ID,"mySidenav").click()
# for i in range(2): #loop through data
#!!!find the elements part:
    #!!find province:
dropdown_province = driver.find_element(By.ID,"cbprovince")
dd= Select(dropdown_province)
dd.select_by_visible_text("ร้อยเอ็ด") #จังหวัด
    #!!find cbamphur:
dropdown_ampur = driver.find_element(By.ID,"cbamphur")
dd= Select(dropdown_ampur)
dd.select_by_visible_text("11-สุวรรณภูมิ") #อำเภอ
    #!!Send number of area:
search = driver.find_element(By.ID,"txtparcelno")
search.send_keys("32645") #เลขที่แปลง 36245
search.send_keys(Keys.RETURN) #Enter;

#!!!Get the location in to array:
time.sleep(3)
Sp = driver.find_element(By.XPATH,"//div[@id='demo1']/div[10]/div[2]").text
arr.append(Sp) #Send the lat,long into Sp array;


#!!!find close button of area's information Popup:
time.sleep(1)
Btn = driver.find_element(By.XPATH,"//div[@id='accordion']/div/div[12]/button[3]").click()


#!!!scroll down to the center:
time.sleep(1)
clickable = driver.find_element(By.CLASS_NAME, "cesium-widget")
ActionChains(driver).click_and_hold(clickable).perform()
ActionChains(driver).move_by_offset( 0, -100).perform()
ActionChains(driver).release().perform()

#!!!zoomout:
driver.execute_script("viewer.camera.zoomOut(350);")

time.sleep(5) #delay for 5sec.
#!!!for capture image:
# driver.execute_script("document.body.style.zoom='70%'")
mapdemo = driver.find_element(By.XPATH,"//div[@id='cesiumContainer']/div/div")
location = mapdemo.location
size = mapdemo.size
mapdemo.screenshot("D:\screen1.png")
# driver.execute_script("document.getElementByTagName('nav').style.zIndex = '-1';")
# driver.save_screenshot("D:\screen.png")

#!!!Crop image:
im = Image.open("D:\screen1.png")
left = location['x'] + 50
top = location['y']
rights = location['x'] + size['width']  - 60
bottom = location['y'] + size['height']
im = im.crop((left, 100, rights, bottom)) # defines crop points
im.save('D:\screen2.png') # saves the new(Crop) image

#!!!clear previous value:
search.clear()
#!!!Close Window:
driver.quit()

#!!!Image Processing Part: #############################################################################################

#!!!Crop The center of image:
img_crop = cv2.imread("D:\screen2.png")
# cv2.rectangle(img, (290,150),(620,400),(0,255,0),3)
roi = img_crop[150:400,290:620]
cv2.imwrite('crop_center_img.png',roi)

#!!!load the image To Processing:
image = cv2.imread("crop_center_img.png")

#!!!grayscale
result = image.copy()
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray,100,200) #Edge.

#!!!adaptive threshold
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,53,7) 

#!!!Fill rectangular contours
cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #find only outside use RETR_EXTERNAL
cv2.drawContours(thresh, cnts, -1, (255,255,255), -1) #draw all contours layer pass -1;

#!!!Morph open
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

#!!!Show the thresh image:
cv2.imshow('thresh', thresh)
cv2.imshow('opening', opening)
#!!!write (save)image;
cv2.imwrite('opening.png',opening) 
cv2.waitKey(0)
cv2.waitKey(0)

#!!!Draw the contours from 'opening' image:
img = cv2.imread("opening.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray,120,200)
contour,hierarchy = cv2.findContours(edge,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
drw = cv2.drawContours(image, contour, -1, (0,255,0), 2) #if need only contour's line change image to img; 
cv2.imshow('drw', drw)
cv2.waitKey(0)

#!!!Save data to csv:
dict = {'province': "ร้อยเอ็ด",'amphur': "11-สุวรรณภูมิ",'location': arr}
df = pd.DataFrame.from_dict(dict)
df.to_csv('Location.csv',encoding="utf-8",index=False)
print(df)




