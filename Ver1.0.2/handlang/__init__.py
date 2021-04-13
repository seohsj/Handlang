from flask import Flask, session, render_template, request
from flask_babel import Babel

def create_app():
    app = Flask(__name__)
    babel = Babel(app)
    app.config['lang_code'] = ['en', 'ko']
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    from . import main_views, quiz, language
    app.register_blueprint(main_views.bp)
    app.register_blueprint(quiz.bp)
    app.register_blueprint(language.bp)

    # app.run(host='0.0.0.0', port=5000, debug=True)
    @app.route('/')
    def index():
        if session.get('language') is None:
            session['language'] = 'ko'
        return render_template('index.html', link=request.full_path)


    @app.route('/aboutUs')
    def aboutUs():
        return render_template('aboutUs.html', link=request.full_path)


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