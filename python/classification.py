import cv2
import mediapipe as mp
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier
import sys

'''
pushUp: 팔굽혀펴기-편 동작, 
pushDown: 팔굽혀펴기-다운 동작
crunchDown: 크런치 누운 동작
crunchUp: 크런치 올라온 동작
'''
actions = ['pushUp', 'pushDown', 'crunchDown', 'crunchUp']

pre = ""
curr = ""

wantExercise = sys.argv[1]

print(sys.argv[1])

color_pose1 = (245,117,66)
color_pose2 = (245,66,230)

#Mediapipe pose model
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5
)

#모델 가져오기
with open("./poseModel.pickle","rb") as fr:
    model = pickle.load(fr)

#웹캠으로 동작, 추후 flask에서 기능 구현 시 수정 필요
cap = cv2.VideoCapture(0)

count = 0

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue

    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = pose.process(img)
    
    mp_drawing.draw_landmarks(
                    img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                    mp_drawing.DrawingSpec(color=color_pose1, thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=color_pose2, thickness=2, circle_radius=2)
                )

    if result.pose_landmarks is not None:
        pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in result.pose_landmarks.landmark]).flatten())
        pose_arr = [pose_row]

        #예측 동작 인덱스, 예측 확률 값
        action = model.predict(pose_arr)
        predic = model.predict_proba(pose_arr)[:6][0]

        curr = actions[action[0]]

        if wantExercise == "pushup" and pre == "pushUp" and curr == "pushDown":
            count += 1
        elif wantExercise == "crunch" and pre == "crunchDown" and curr == "crunchUp":
            count += 1
        
        pre = curr

        cv2.putText(img, text=actions[action[0]], org=(25,25), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
        cv2.putText(img, text=("%.2f" % predic[action[0]]), org=(25,75), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)
        cv2.putText(img, text=("%d" % count), org=(25,125), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)


    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('pose', img)

    if cv2.waitKey(1) == ord('q'):
        break