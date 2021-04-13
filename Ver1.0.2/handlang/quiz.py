from flask import url_for, render_template, request, redirect
import json
import random
from flask import Blueprint


bp = Blueprint('quiz', __name__, url_prefix='/quiz')

    
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
    def get_letter_list(self):
        # alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o',
        #              'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
        return self.__letter_list
    def letter_list_idx(self,element):
        next_topic = ""
        previous_topic = ""
        letter_list=self.__letter_list
        list_idx_end = len(letter_list) - 1  # 마지막 인덱스
        idx_now = letter_list.index(element)
        if idx_now == list_idx_end:
            next_topic = letter_list[0]
        else:
            next_topic = letter_list[idx_now + 1]
        if idx_now != 0:
            previous_topic = letter_list[idx_now - 1]
        return next_topic, previous_topic
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
    


total_q = 5


def make_quiz(language_model):
    question_list = {}
    img_list = []
    for i in range(total_q):
        question, examples, img = make_random_quiz(question_list,language_model)
        question_list[question] = examples
        img_list.append(img)
    return question_list, img_list


def make_random_quiz(question_list,language_model):
    alphabet_list = language_model.get_letter_list()
    examples = []  # 보기
    while True:
        answer = alphabet_list[random.randint(0, len(alphabet_list) - 1)]
        if is_valid_quiz(answer, question_list):
            break
    examples.append(answer)
    while len(examples) != 4:
        randomIndex = random.randint(0, len(alphabet_list) - 1)
        if alphabet_list[randomIndex] not in examples:
            examples.append(alphabet_list[randomIndex])
    random.shuffle(examples)
    img = []
    for i in examples:
        img.append('../static/img/asl_' + i + ".png")

    return answer, examples, img


# 이전에 낸 문제인지 확인
def is_valid_quiz(answer, question_list):
    if answer in question_list:
        return False
    else:
        return True


@bp.route('/<group>', methods=['GET', 'POST'])
def quiz(group):
    if request.method == 'GET':
        language_model=get_model(group)
        question_list, img_list = make_quiz(language_model)
        print(question_list)
        return render_template('quiz/question.html',group=group, str=str, enumerate=enumerate, question_list=question_list,
                               img_list=img_list, total_q=total_q, link=request.full_path)

    if request.method == 'POST':
        user_answers = {}
        for i in range(total_q):
            question = "question" + str(i)
            answer = "answer" + str(i)
            q = request.form[question]
            a = request.form[answer]
            user_answers[q] = a
            print(user_answers)
        user_answers = json.dumps(user_answers)

        return redirect(url_for('quiz.quiz_result',group=group, user_answers=user_answers))


@bp.route('/<group>/result')
def quiz_result(group):
    try:
        user_answers = json.loads(request.args['user_answers'])
        items = user_answers.items()
    except:
        user_answers = {}
    items = user_answers.items()
    correct_num = 0
    incorrect_questions = []
    for q, a in items:
        if (q == a):
            correct_num += 1
        else:
            incorrect_questions.append(q.upper())

    if correct_num == total_q:
        img_path = "score_100.png"
    elif correct_num >= (total_q // 2):
        img_path = "score_50.png"
    else:
        img_path = "score_0.png"
    print(img_path)
    return render_template('quiz/result.html', group=group,correct_num=correct_num, incorrect_questions=incorrect_questions,
                           total_q=total_q, img_path=img_path, link=request.full_path)

