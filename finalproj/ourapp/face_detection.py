
import os
import cv2
import numpy as np 
from PIL import Image

def train_classifier(data_dir):
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    print(path)
    haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    features = []
    ids = []
    
    for image in path:
        print(image)
        # img = Image.open(image).convert('L')
        img=cv2.imread(image)
        
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        face_rect=haar_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        id = int(os.path.split(image)[1].split(".")[1])
       
        print(id)
        for x,y,w,h in face_rect:
            faces_region_of_int = gray[y:y+h, x:x+w]
            features.append(faces_region_of_int)
            ids.append(id)
        
        
    #     # id1s = os.path.split(image)
    print(ids)
    print(features)

        
        
    print(f'Length of  features={len(features)}')
    print(f'Length of  labels={len(ids)}')    
    ids_ary = np.array(ids)
    features_ary=np.array(features,dtype=object)
   
    
    # Train and save classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(features_ary,ids_ary)
    clf.save("classifier.xml")
train_classifier("data")
