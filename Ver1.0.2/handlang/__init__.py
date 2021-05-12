from flask import Flask, session, request
from flask_babel import Babel

def create_app():
    app = Flask(__name__)
    babel = Babel(app)
    app.config['lang_code'] = ['en', 'ko']
    app.secret_key = 'super secret key' #csrf?
    app.config['SESSION_TYPE'] = 'filesystem'


    from . import home , practice, language, quiz
    app.register_blueprint(practice.bp)
    app.register_blueprint(quiz.bp)
    app.register_blueprint(language.bp)
    app.register_blueprint(home.bp)


    @babel.localeselector
    def get_locale():
        try:
            language = session['language']
        except KeyError:
            language = None
        if language is not None:
            return language
        return request.accept_languages.best_match(['en', 'ko'])

    return app