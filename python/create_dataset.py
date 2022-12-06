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

#AI-Hub에서 피트니스 이미지 데이터를 사용할 계획
#운동의 각 구분동작 별로 데이터셋 폴더 나눔
#knn알고리즘으로 각 구분 동작 학습

#csv는 반복 전 열어 각 반복마다 학습한 값과 라벨을 각 row에 저장
dataset = open("dataset.csv", "w", newline='')

#actions의 크기만큼 반복
for idx, action in enumerate(actions):
    #actions의 각 명칭별로 있는 폴더 안의 이미지 사용
    img_path = "python/data/" + action + '/'
    file_list = os.listdir(img_path)
    for img_file in file_list:
        #각 이미지 별로 포즈 학습
        img = cv2.imread(img_path + img_file, cv2.IMREAD_COLOR)

        result = pose.process(img)

        #학습 데이터에서 프즈를 제대로 인식하는지 cv2에 랜드마크 추가해 확인
        mp_drawing.draw_landmarks(
                    img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                    mp_drawing.DrawingSpec(color=color_pose1, thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=color_pose2, thickness=2, circle_radius=2)
                )

        if result.pose_landmarks is not None:

            cv2.imshow('img', img)
            cv2.waitKey(500)

            #랜드마크가 정상 인식 되었을 경우 csv파일에 저장
            try:
                pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in result.pose_landmarks.landmark]).flatten())
                pose_row.append(idx)
                print(pose_row)
                csv_writer = csv.writer(dataset, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(pose_row)
            except:
                pass
