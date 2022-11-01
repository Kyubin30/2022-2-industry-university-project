import cv2
import mediapipe as mp
import numpy as np
import time, os

#exer1: 팔굽혀펴기
actions = ['exr1']
seq_length = 30
secs_for_action = 30

#Mediapipe pose model
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    model_complexity=2,
    min_detection_confiendce=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

created_time = int(time.time())
os.makedirs('dataset', exist_ok=True)