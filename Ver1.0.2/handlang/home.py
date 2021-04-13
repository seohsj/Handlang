from flask import session, render_template, request
from flask import Blueprint


bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
    if session.get('language') is None:
        session['language'] = 'ko'
    return render_template('home/index.html', link=request.full_path)


@bp.route('/aboutUs')
def aboutUs():
    return render_template('home/aboutUs.html', link=request.full_path)

