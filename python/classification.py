import cv2
import mediapipe as mp
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier

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
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5
)

#모델 가져오기
with open("./poseModel.pickle","rb") as fr:
    model = pickle.load(fr)

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

        cv2.putText(img, text=actions[action[0]], org=(50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)
        cv2.putText(img, text=("%.2f" % predic[action[0]]), org=(400,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)
        cv2.putText(img, text=("%d" % count), org=(600,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)


    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('pose', img)

    if cv2.waitKey(1) == ord('q'):
        break