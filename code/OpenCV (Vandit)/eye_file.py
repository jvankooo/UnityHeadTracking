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

# xml file location varies from PC to PC
face_cascade = cv2.CascadeClassifier(r'C:\Users\vandi\PycharmProjects\untitled\venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(r'C:\Users\vandi\PycharmProjects\untitled\venv\Lib\site-packages\cv2\data\haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            print("X Co-ordinate =")
            print(ex+(ew/2))
            print("Y Co-ordinate =")
            print(ey+(eh/2))
            print("\n")
            data = str(ex+(ew/2))
            sock.sendto(data.encode(), (UDP_IP, UDP_PORT))
            data = str(ey+(eh /2))
            sock.sendto(data.encode(), (UDP_IP, UDP_PORT))

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()