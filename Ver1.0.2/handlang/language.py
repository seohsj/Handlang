from flask import  request, redirect, session
from flask import Blueprint


bp = Blueprint('language', __name__, url_prefix='/')

@bp.route('/english')
def english():
    session['language'] = 'en'
    link = request.args.get('link')
    if link:
        return redirect(link)
    else:
        return redirect('/')


@bp.route('/korean')
def korean():
    session['language'] = 'ko'
    link = request.args.get('link')
    if link:
        return redirect(link)
    else:
        return redirect('/')
