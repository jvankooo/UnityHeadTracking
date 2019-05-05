import cv2
import time
import pandas
from datetime import datetime
import numpy as np
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

flag = True

# xml file location varies from PC to PC
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(1)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width, channels = img.shape
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    maxArea = 0
    var = [0,0,0,0]
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        area = w*h
        print(area, "\n")
        # find main player face
        if area >= maxArea:
            maxArea = area
            var[0]=x
            var[1]=y
            var[2]=w
            var[3]=h

    if maxArea > 0:

        if flag == True:
            intArea = maxArea
            flag = False
        # mark player face
        cv2.rectangle(img, (var[0], var[1]), (var[0] + var[2], var[1] + var[3]), (0, 255, 0), 5)

        #interpolate angle from -60 to 60 degrees
        angleX = np.interp(var[0]+var[2]/2, (0+var[2]/2, width-var[2]/2), (-60, 60)) 
        angleY = np.interp(var[1]+var[3]/2, (0+var[3]/2, height-var[3]/2), (-20, 20))

        #interpolate zoom factor
        zoom = np.interp(maxArea, (0, intArea, 2*intArea), (-20, 0, 20))
        print('X=', angleX, 'Y=', angleY, 'A=', zoom, "\n")    
        data = str(angleX) + 'n' + str(angleY) + 'n' + str(zoom)
        sock.sendto(data.encode(), (UDP_IP, UDP_PORT))   

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()