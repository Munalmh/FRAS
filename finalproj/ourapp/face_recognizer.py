
import cv2
import numpy as np
from PIL import Image
import os
import datetime
import time

def attendance(name,id):
    with open('Atttendence.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now_date=datetime.datetime.now()
            dtstring=now_date.strftime("%Y:%m:%d")
            f.writelines(f'\n{name},{dtstring},{id}')

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    
    for (x,y,w,h) in features:
        cv2.rectangle(img, (x,y), (x+w,y+h), color, 2 )
        
        id, pred = clf.predict(gray_img[y:y+h,x:x+w])
        confidence = int(100*(1-pred/300))
        
        if confidence>50:
            if id==1:
                cv2.putText(img, "Keshab", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                attendance("Keshab",id)
            if id==2:
                cv2.putText(img, "Asbin", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                attendance("Asbin",id)
        else:
            cv2.putText(img, "UNKNOWN", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)
    
    return img

# loading classifier
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.xml")

video_capture = cv2.VideoCapture(0)

while True:
    ret, img = video_capture.read()
    img = draw_boundary(img, faceCascade, 1.3, 6, (255,255,255), "Face", clf)
    cv2.imshow("face Detection", img)
    
    if cv2.waitKey(5)==13:
        break
video_capture.release()
cv2.destroyAllWindows()