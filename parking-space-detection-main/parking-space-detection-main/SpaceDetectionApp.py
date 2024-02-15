#############  REAL TIME PARKING SPACE DETECTION  ##############

import cv2
import pickle
import cvzone
import numpy as np

width,height=210,100

#DOWNLOAD IP WEBCAM IN MOBILE, START YOUR SERVER, ENTER THE IP

cam="<YOUR IP>/video"

#####   SELECTING AREA TO DETECT EMPTY SPACE   #####
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []
    
def mouseClick1(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)            
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)
        
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.open(cam)
print("Check::",cap.isOpened())
fourcc=cv2.VideoWriter_fourcc(*"XVID")
output=cv2.VideoWriter("Output.avi",fourcc,20.0,(600,400),0)
while True:
    _,img= cap.read()
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

#####   FUCTION TO PERFORM SCANNING THE SELECTED AREA   #####

booklst=[]
posList1=[]
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

def checkParkingSpace(imgPro):
    spaceCounter = 0
 
    for pos in posList:
        x, y = pos
 
        imgCrop = imgPro[y:y + height, x:x + width]
        #cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
 
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)
    
    cvzone.putTextRect(img, f'Slots Available: {spaceCounter-len(booklst)}/{len(posList)}', (0, 625), scale=3,
                           thickness=3, offset=20, colorR=(0,255,0))
    cvzone.putTextRect(img, f'Slots Booked: {len(booklst)}/{len(posList)}', (800, 625), scale=3,
                           thickness=5, offset=20, colorR=(0,255,255))
    
def mouseClick2(events, x, y, flags, params):
    if events == cv2.EVENT_MBUTTONDOWN:
        for i, pos in enumerate(posList1):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList1.pop(i)
                booklst.pop((i))
    if events == cv2.EVENT_LBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                booklst.append(i)
                #cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 6)
   
    if events == cv2.EVENT_RBUTTONDOWN:
        posList1.append((x, y))
        booklst.append((x,y))
        
    if events == cv2.EVENT_LBUTTONDBLCLK:
        for i, pos in enumerate(posList1):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList1.pop(i)
                booklst.pop(i)

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.open(cam)
print("Check::",cap.isOpened())
fourcc=cv2.VideoWriter_fourcc(*"XVID")
output=cv2.VideoWriter("Output.avi",fourcc,20.0,(600,400),0)

while(cap.isOpened()):
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
 
    checkParkingSpace(imgDilate)
    for pos in posList1:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 255), 2)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
