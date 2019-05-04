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
w_MAX = 500
d_MIN = 10

# xml file location varies from PC to PC
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

cap = cv2.VideoCapture(1)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width, channels = img.shape
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        dist = (w_MAX*w_MAX*d_MIN)/(w*w)
        #print('d = ', dist, '\n')
        angleX = 2*np.interp((x+w/2)/dist, (0, width/dist), (-30, 30)) #interpolate from -30 to 30 degrees
        angleY = 2*np.interp((y+h/2)/dist, (0, height/dist), (-30, 30))
        print('X=', angleX, 'Y=', angleY, "\n")    
        data = str(angleX) + 'n' + str(angleY)
        sock.sendto(data.encode(), (UDP_IP, UDP_PORT))

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()