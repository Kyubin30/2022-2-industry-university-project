# AI 운동 PT 어플리케이션 🤸‍♂️
## 2022-2학기 충북대학교 산학프로젝트 두원빌라 조
mediapipe를 활용한 포즈 인식 AI를 통해 홈트를 보다 편리하도록 즐기기 위해 제작한 어플리케이션
<br><br>
<img src="logo.png" style="display: flex; width: 200px;">
<br>
노션: https://kyubin30.notion.site/AI-PT-ea2df1a2d9484a72831be6311a78643f


## Contact

- 이규빈(Kyubin30)    : leekebin3@naver.com
- 고종현(jonghyunko)  : rhwhdgus1223@naver.com
- 유준호(junhoyoo00)  : juno2744@naver.com

## Description
python/ <br>
- create_dataset.py : 
<br>데이터셋 제작 파일, data 폴더 생성 후 actions의 각 인덱스에 맞는 폴더 생성 후 이미지를 넣으면 dataset.csv 파일 생성
- train.ipynb : 
<br> dataset.csv 파일을 이용하여 knn알고리즘을 이용한 사용자 동작 분류 모델 생성, poseModel.pickle 파일로 저장
- classification.py : 
<br> 만들어진 poseModel.pickle 파일을 이용해 사용자의 현재 동작 예측, 운동 횟수 체크 등을 수행

<br> flask/ <br>
- app.py :
<br> flask 웹 서버 생성, 기본 루트는 운동 리스트를 선택하는 detailPage.html이고, 리스트를 선택하면 운동 동영상 및 설명 페이지로 이동한다. 사용자가 운동 시작 버튼을 누르면 streaming.html 페이지로 이동하고 classigication.py의 동작을 수행한다. stop 버튼을 누르면 <i>result.html(현재 미구현)</i>로 이동한다. 

## Dependency
- python 3.9.7
- OpenCV
- mediapipe
- bootstrap 5
- sklearn 1.1.3
- numpy
- flask
- pandas
- matplotlib
- seaborn
- android studio


## Install
```
conda create --name [env_name]  python=3.9
conda activate [env_name]
pip install opencv-python==4.6
pip install sklearn==1.1.3
pip install tensorflow-gpu==2.11.0
pip install mediapipe==0.8.10.1
pip install flask
```
**모델 파일의 제작 버전은 sklearn 1.1.3입니다.<br>이외의 버전으로 모델을 실행할 경우 오류가 발생할 수 있습니다.** <br><br>
classification.py의 경우 실행 시 arg값이 필요합니다.<br>
예시
```
python classification.py pushup
```



## 참고
https://github.com/kairess/gesture-recognition <br>
https://github.com/dawi9840/mediapipe_pose_classification_with_tf

