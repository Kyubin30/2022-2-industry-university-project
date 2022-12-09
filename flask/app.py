
from flask import Flask, render_template, request, Response, jsonify, url_for
import cv2
import mediapipe as mp
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)

actions = ['pushUp', 'pushDown']

pre = ""
curr = ""

count = 0

color_pose1 = (245,117,66)
color_pose2 = (245,66,230)

camera = cv2.VideoCapture(0)

#Mediapipe pose model
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5
)

with open("flask/poseModel.pickle","rb") as fr:
    model = pickle.load(fr)

#운동 목록
exerciseList = {
    "pushup" : "팔굽혀펴기",
    "crunch" : "크런치"
}

def counting():
    if pre == "pushUp" and curr == "pushDown":
        count += 1


#프레임 생성 
def gen_frames():
    while True:
        success, frame = camera.read()

        img = cv2.flip(frame, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = pose.process(img)

        if result.pose_landmarks is not None:

            mp_drawing.draw_landmarks(
                    img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                    mp_drawing.DrawingSpec(color=color_pose1, thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=color_pose2, thickness=2, circle_radius=2)
                )

            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in result.pose_landmarks.landmark]).flatten())
            pose_arr = [pose_row]

            #예측 동작 인덱스, 예측 확률 값
            action = model.predict(pose_arr)
            predic = model.predict_proba(pose_arr)[:6][0]

            curr = actions[action[0]]

            counting()

            pre = curr

            cv2.putText(img, text=actions[action[0]], org=(50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)
            cv2.putText(img, text=("%.2f" % predic[action[0]]), org=(400,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)
            cv2.putText(img, text=("%d" % count), org=(600,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, color=(0, 0, 255), thickness=3)

        
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

#초기 리스트 페이지
@app.route("/")
def homepage():
   return 'coeni'

#get을 이용하여 리스트 페이지의 운동 이름을 가져옴
@app.route("/detail", methods=['GET']) 		
def hello_request():
    data = request.args.get('exercise')
    #jsonify(data)
    return render_template("detailPage.html", exerciseEng = data, exerciseKor = exerciseList[data])

#비디오 및 미디어 파이프 작동 라우터
@app.route('/video_feed')
def video_feed():
    count = 0
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#video_feed show 라우터
@app.route('/streaming')
def index():
    """Video streaming home page."""
    return render_template('streaming.html')

if __name__ == '__main__':
    app.run(debug=True)