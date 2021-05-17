from flask import url_for, render_template, request, redirect,  g
import json
import random
from flask import Blueprint
from .common import SignLanguage

bp = Blueprint('quiz', __name__, url_prefix='/quiz')


@bp.before_app_request
def quiz_info():
    g.number_of_quiz = 5
    g.number_of_choice = 4



@bp.route('/<group>', methods=['GET', 'POST'])
def _list(group):
    if request.method == 'GET':
        question_list= make_quiz(group)
        print(question_list)
        return render_template('quiz/list.html',group=group, enumerate=enumerate, question_list=question_list,
                                total_q=g.number_of_quiz)


    if request.method == 'POST':
        incorrect_questions = []
        correct_num = 0
        for i in range(g.number_of_quiz ):
            question = "question" + str(i)
            answer = "answer" + str(i)
            q = request.form[question]
            a = request.form[answer]
            if(q==a):
                correct_num += 1
            else:
                incorrect_questions.append(q.upper())


        incorrect_questions = json.dumps(incorrect_questions)
        return redirect(url_for('quiz.result',group=group, correct_num = correct_num , incorrect_questions=incorrect_questions))


@bp.route('/<group>/result')  #http://127.0.0.1:5000/quiz/number/result?correct_num=0&incorrect_questions=%5B%227%22%2C+%225%22%2C+%223%22%2C+%226%22%2C+%222%22%5D
def result(group):
    try:
        incorrect_questions = json.loads(request.args['incorrect_questions'])
        correct_num = int(request.args['correct_num'])

    except:
        #예외처리
          incorrect_questions = []
          correct_num=0
 
    if correct_num == g.number_of_quiz :  #점수에 따라서 그림을 다르게 하는 것
        img_path = "score_100.png"
    elif correct_num >= (g.number_of_quiz  // 2):
        img_path = "score_50.png"
    else:
        img_path = "score_0.png"
    return render_template('quiz/result.html', group=group,correct_num=correct_num, incorrect_questions=incorrect_questions,
                           total_q=g.number_of_quiz , img_path=img_path)


def make_quiz(group):
    letter_list=SignLanguage.get_letter_list(group)
    questions = []
    try:
        questions= random.sample(letter_list, g.number_of_quiz )
    except ValueError:
        print("전체 질문 수(number_of_quiz)가 ", len(letter_list),"를 넘습니다.")  

    quiz_list={}
    for question in questions:
        choices= make_random_choices(letter_list, question)
        quiz_list[question]=choices
    
    return quiz_list


def make_random_choices(letter_list, question):
    c_letter_list=letter_list[:] 
    c_letter_list.remove(question)
    try:
        choices = random.sample(c_letter_list, g.number_of_choice - 1)
    except ValueError:
        print("전체 선지 수(number_of_choice)가 ", len(c_letter_list),"를 넘습니다.") #https://flask.palletsprojects.com/en/2.0.x/errorhandling/

    choices.append(question)
    random.shuffle(choices)
    
    return choices


