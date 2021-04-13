from flask import render_template, Response, request, redirect, g, session
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import numpy as np
import cv2
import json
from flask_babel import Babel, gettext
import tensorflow as tf
from tensorflow.python.keras.backend import set_session
from flask import Blueprint
from .common import SignLanguage


bp = Blueprint('practice', __name__, url_prefix='/')


sess = tf.Session()
graph = tf.get_default_graph()


set_session(sess)
# alphamodel = load_model('model/handlang_model_4.h5')
# numbmodel = load_model('model/su_adamax.h5')

print("Loaded model from disk")


    
class Models:
    def __init__(self,label,letter_list):
        self.__label=label
        self.__letter_list=letter_list
    
    def get_label(self,idx):
        # label = ["A", "B", "C", "D", "E", "F", "G",
        #     "H", "I", "K", "L", "M", "N", "O", "P", "Q",
        #     "R", "S", "T", "U", "V", "W", "X", "Y",
        #     "del", "nothing", "space"]
        return self.__label[idx]

    # def letter_list_idx(self,element):
    #     next_topic = ""
    #     previous_topic = ""
    #     letter_list=self.__letter_list
    #     list_idx_end = len(letter_list) - 1  # 마지막 인덱스
    #     idx_now = letter_list.index(element)
    #     if idx_now == list_idx_end:
    #         next_topic = letter_list[0]
    #     else:
    #         next_topic = letter_list[idx_now + 1]
    #     if idx_now != 0:
    #         previous_topic = letter_list[idx_now - 1]
    #     return next_topic, previous_topic
alphabet_label=["A", "B", "C", "D", "E", "F", "G",
             "H", "I", "K", "L", "M", "N", "O", "P", "Q",
            "R", "S", "T", "U", "V", "W", "X", "Y",
            "del", "nothing", "space"]
alphabet_list=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o',
                      'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']

number_label = ["0","1","2","3","4","5","6","7","8","9","del", "nothing", "space"]
number_list = ['0','1','2','3','4','5','6','7','8','9']
alphabet_model=Models(alphabet_label,alphabet_list)
number_model= Models(number_label, number_list) 


def get_model(group):
    if group=="alphabet":
        return alphabet_model
    if group=="number":
        return number_model
    


# ** 전역변수 대신 클래스 객체 사용
class PredictLabel(object):
    def __init__(self, label):
        self.label = label

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label

class Target_idx(object):
    def __init__(self, idx):
        self.idx = idx

    def set_idx(self, idx):
        self.idx = idx

    def get_idx(self):
        return self.idx

target_idx = Target_idx(0)
predict_label = PredictLabel('')

# 
total_q = 5




# def gen(camera,group):
#     global alphamodel
#     global numbmodel
#     if not camera.isOpened():
#         raise RuntimeError("Could not start camera")
#     if(group=='alphabet'):
#         model=alphamodel
#     else:
#         model = numbmodel

#     while True:
#         success, img = camera.read() #이미지를 프레임단위로 잘라
#         if success:
#             try:
                
#                 cv2.rectangle(img, (250,250), (600,600), (000,51,51), 2)

#                 crop_img = img[250:600, 250:600] #이미지를 잘라서 보여주므로 카메라에 보이는 화면이 확대되어 보여진다.
#                 # crop_img_path = crop_img_origin_path.get_path_name() + '/crop_img.jpg'
#                 # cv2.imwrite(crop_img_path, img)
                
                
#                 image=cv2.resize(crop_img, (64, 64)) #model에서 input이 64, 64 ,3 이므로
#                 # print(image.shape)

#                 # image = load_img(crop_img_path, target_size=(64,64))

#                 # image = img_to_array(image)
#                 # print(image.shape)
#                 image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
#                 global sess
#                 global graph
#                 with graph.as_default():
#                     set_session(sess)
#                     prediction = model.predict(image)

#                 target_idx_for_predict = target_idx.get_idx()
#                 # print("타겟예측: ", prediction[0][target_idx_for_predict])
#                 print(get_model(group).get_label(target_idx_for_predict))

#                 print(prediction[0])
#                 print(np.argmax(prediction[0]))                
#                 # print(get_model(group).get_label(np.argmax(prediction[0])))
#                 if np.argmax(prediction[0]) == 1:
#                     result = get_model(group).get_label(np.argmax(prediction[0]))

#                 elif prediction[0][target_idx_for_predict] > 0: 
#                     result = get_model(group).get_label(target_idx_for_predict)
#                 else:
#                     result = ''

#                 predict_label.set_label(result)
#                 # print("===gen===start")
#                 # print(result)
#                 # print(predict_label.get_label())
#                 # print("===gen===end")
#                 # print("\n")
#                 ret, jpeg = cv2.imencode('.jpg', crop_img)
#                 frame = jpeg.tobytes()

#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#             except Exception as e:
#                 print("An exception occurred",e)

#         else:
#             print("Status of camera.read()\n", success, "\n=======================")





@bp.route('/return_label', methods=['POST', 'GET'])
def return_label():
    value = request.form.get("target", False)
    # 띄어쓰기 조심!@!
   
    label_list = [" A ", " B ", " C ", " D ", " E ", " F ", " G ",
            " H ", " I ", " J ", " K ", " L ", " M ", " N ", " O ", " P ", " Q ", 
            " R ", " S ", " T ", " U ", " V ", " W ", " X ", " Y ", " Z ", 
            " del ", " nothing ", " space "]
    
    tem = label_list.index(value)
    print(tem)
    print("label")
    idx = target_idx.set_idx(tem)
    # print(idx)
    label = " " + predict_label.get_label() + " "
    print(label)

    # ajax 에서 값 받아올때 공백이 앞뒤로 붙는데 python strip() 함수가 안먹어서...

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

@bp.route('/return_label2', methods=['POST', 'GET'])
def return_label2():
    value = request.form.get("target", False)
    # 띄어쓰기 조심!@!
   
    label_list = [" 0 ", " 1 "," 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 ", " del ", " nothing ", " space "]

    
    tem = label_list.index(value)
    print(tem)
    # idx = target_idx.set_idx(tem)
    # print(idx)
    label = " " + predict_label.get_label() + " "
    print(label)
    # ajax 에서 값 받아올때 공백이 앞뒤로 붙는데 python strip() 함수가 안먹어서...

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


# # video streaming
# @bp.route('/<group>/video_feed')
# def video_feed(group):
#     camera = cv2.VideoCapture(0)
#     return Response(gen(camera,group), mimetype='multipart/x-mixed-replace; boundary=frame')
# video streaming
@bp.route('/<group>/video_feed')
def video_feed(group):
    camera = cv2.VideoCapture(0)
    return "hello"



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