from flask import url_for, render_template, request, redirect
import json
import random
from flask import Blueprint
from .common import SignLanguage

bp = Blueprint('quiz', __name__, url_prefix='/quiz')

total_q = 5

@bp.route('/<group>', methods=['GET', 'POST'])
def quiz(group):
    if request.method == 'GET':
        question_list, img_list = make_quiz(group)
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

def make_quiz(group):
    question_list = {}
    img_list = []
    for i in range(total_q):
        question, examples, img = make_random_quiz(question_list,group)
        question_list[question] = examples
        img_list.append(img)
    return question_list, img_list


def make_random_quiz(question_list,group):
    alphabet_list = SignLanguage.get_letter_list(group)
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