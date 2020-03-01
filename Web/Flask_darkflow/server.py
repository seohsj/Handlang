from flask import Flask, url_for, render_template, Response
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf
import threading
import numpy

app = Flask(__name__)

# ajax 통신 변수
tem_message = "temporary"
final_message = "prediction result"

# options = {"model": "./cfg/handlang-small.cfg",
#            "pbLoad": "./darkflow/built_graph/handlang-small.pb",
#            "metaLoad": './darkflow/built_graph/handlang-small.meta' , "threshold": 0.4}

options = {"model": "./cfg/yolo.cfg", "load": "./bin/yolo.weights", "threshold": 0.4}

tfnet = TFNet(options)

def checkResult(label):
    tem_message = label

def gen(camera):
    sess = tf.Session()
    with sess.as_default():
        while True:
            success, img = camera.read()
            if success:
                    results = tfnet.return_predict(img)

                    for result in results:
                        label = result["label"] # 예측값
                        confidence = result["confidence"] # 신뢰도

                        cv2.rectangle(img,
                                    (result["topleft"]["x"], result["topleft"]["y"]),
                                    (result["bottomright"]["x"], result["bottomright"]["y"]),
                                    (255, 0, 0), 4)
                        text_x, text_y = result["topleft"]["x"] - 10, result["topleft"]["y"] - 10
                        cv2.putText(img, result["label"], (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (0, 255, 0), 2, cv2.LINE_AA)
                        
                        # 예측값이랑 신뢰도 같이 프린트해서 보여주기 (기존 것 위에 계속 출력)
                        global tem_message
                        tem_message = label
                        print("result: ", label, "| confidence: ", confidence)

                    #cv2.imshow('frame',img)

                    ret, jpeg = cv2.imencode('.jpg', img)
                    frame = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            else:
                print("Status of camera.read()\n", success, img, "\n=======================")

# ajax 통신 함수
@app.route("/sendResult")
def sendResult():
    global tem_message, final_message

    if tem_message == "temporary":
        final_message = "no prediction yet"

    else:
        final_message = tem_message

    return final_message

@app.route('/video_feed')
def video_feed():
    cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def webcam():
    return render_template('webcam.html', resultReceived=sendResult())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
