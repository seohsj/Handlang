from flask import render_template, Response, request, redirect, g, session
from keras.models import load_model
import numpy as np
import cv2
import json
from flask_babel import Babel, gettext
from flask import Blueprint
from .common import SignLanguage



bp = Blueprint('practice', __name__, url_prefix='/')


predict_label = ''  ##

# video streaming
@bp.route('/<group>/video_feed')
def video_feed(group):
    target_label = request.args.get('alphabet')
    camera = cv2.VideoCapture(0)
    target_idx_for_predict=SignLanguage.get_label_idx(group, target_label)
    return Response(gen(camera,group,target_idx_for_predict), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera,group,target_idx_for_predict):

    if not camera.isOpened():
        raise RuntimeError("Could not start camera")
    if(group=='alphabet'):
        print("loadmodel")
        model = load_model('handlang/model/handlang_model_4.h5')
    else:
        print("loadmodel")
        model = load_model('handlang/model/su_adamax.h5')

    while True:
        success, img = camera.read() #이미지를 프레임단위로 잘라
        if success:
            try:
                
                cv2.rectangle(img, (250,250), (600,600), (000,51,51), 2)

                crop_img = img[250:600, 250:600] #이미지를 잘라서 보여주므로 카메라에 보이는 화면이 확대되어 보여진다.
                
                
                image=cv2.resize(crop_img, (64, 64)) #model에서 input이 64, 64 ,3 이므로


                image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
                prediction = model.predict(image)
                print("타겟예측: ", prediction[0][target_idx_for_predict])
                print("target_idx_for_predict",target_idx_for_predict)
                print(prediction[0])
                print(np.argmax(prediction[0]))  

                argmaxIdx = np.argmax(prediction[0])

                if prediction[0][argmaxIdx] == 1:
                    result =  SignLanguage.get_label( group, argmaxIdx )

                elif prediction[0][target_idx_for_predict] > 0: 
                    result = SignLanguage.get_label( group, target_idx_for_predict )
                else:
                    result = ''

                global predict_label
                predict_label=result
     
                ret, jpeg = cv2.imencode('.jpg', crop_img)
                frame = jpeg.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            except Exception as e:
                print("An exception occurred",e)

        else:
            print("Status of camera.read()\n", success, "\n=======================")





@bp.route('/return_label', methods=['POST', 'GET'])
def return_label():
    value = request.form.get("target", False)
    global predict_label
    label = predict_label

    if label == '':
        predict_result = {
            'status': 0,
            'info': 'not detected',
            'label': '',
            'lang_code': session['language']
        
        }
    elif label != value:
        predict_result = {
            'status': 0,
            'info': gettext('predict_incorrect'),
            'label': label,
            'lang_code': session['language']

        }
        print("틀림!")
    else:
        predict_result = {
            'status': 1,
            'info': gettext('predict_correct'),
            'label': label,
            'lang_code': session['language']
        }

    # result 의 status 값이 1이면 참 -> main.js 에서 correct 값 증가

    json_data = json.dumps(predict_result)  # json 형태로 바꿔줘야 에러 안남
    return json_data



@bp.route('/<group>')
def practice_list(group):
    alphabet_list = SignLanguage.get_letter_list(group)
    return render_template('practice/practice_list.html',group=group , alphabet_list=alphabet_list, link=request.full_path)



@bp.route('/<group>/practice', methods=['GET', 'POST'])
def practice(group):
    element = request.args.get('element')
    if(group=='alphabet'):
        alphabet=element.upper()
    else:
        alphabet=element

    img = "../static/img/asl_" + element + ".png"

    next_topic, previous_topic = getNextPrevTopic(group, element)

    return render_template('practice/practice_model.html',group=group,alphabet=alphabet, img=img, previous_topic=previous_topic,
                           next_topic=next_topic, link=request.full_path)



def getNextPrevTopic(group,element):
    next_topic = ""
    previous_topic = ""
    letter_list = SignLanguage.get_letter_list(group)
    list_idx_end = len(letter_list) - 1  # 마지막 인덱스
    idx_now = letter_list.index(element)
    if idx_now == list_idx_end:
        next_topic = letter_list[0]
    else:
        next_topic = letter_list[idx_now + 1]
    if idx_now != 0:
        previous_topic = letter_list[idx_now - 1]
    return next_topic, previous_topic

    