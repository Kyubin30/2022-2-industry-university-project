
from flask import Flask, render_template, request, Response, jsonify, url_for
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)

exerciseList = {
    "pushup" : "팔굽혀펴기",
    "crunch" : "크런치"
}

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

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

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/streaming')
def index():
    """Video streaming home page."""
    return render_template('streaming.html')

if __name__ == '__main__':
    app.run(debug=True)