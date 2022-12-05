import cv2
import mediapipe as mp
import numpy as np
import os
import csv

'''
pushUp: 팔굽혀펴기-편 동작, 
pushDown: 팔굽혀펴기-다운 동작
'''
actions = ['pushUp', 'pushDown']

color_pose1 = (245,117,66)
color_pose2 = (245,66,230)

#Mediapipe pose model
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue

    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    ##cv2.putText(img, text=text, org=(int(img.shape[1] / 2), 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)
    
    if cv2.waitKey(1) == ord('q'):
        break