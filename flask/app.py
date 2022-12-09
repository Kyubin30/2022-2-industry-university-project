
from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)

exerciseList = {
    "pushup" : "팔굽혀펴기",
    "crunch" : "크런치"
}

#초기 리스트 페이지
@app.route("/")
def homepage():
   data = list(exerciseList.keys())
   return render_template("index.html", data = data) 

#get을 이용하여 리스트 페이지의 운동 이름을 가져옴
@app.route("/detail", methods=['GET']) 		
def hello_request():
    data = request.args.get('exercise')
    #jsonify(data)
    return render_template("detailPage.html", exerciseEng = data, exerciseKor = exerciseList[data])

if __name__ == '__main__':
    app.run(debug=True)