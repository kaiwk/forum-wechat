import os
import logging
import logging.config

from werkzeug.exceptions import HTTPException

from flask import Flask, redirect, Response


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


def create_app(test_config=None):
    """
    Create and configure an instance of the Flask application.

    Some config variable we need to specify in 'instance/config.py'

    DEBUG
    SECRET_KEY
    GITHUB_SECRET
    REPO_PATH
    """
    fapp = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(fapp.instance_path)
    except OSError:
        pass

    # a default secret that should be overridden by instance config
    fapp.config.from_mapping(
        SECRET_KEY='this-is-a-secret-key'
    )

    if test_config is None:
        if fapp.config['ENV'] == 'local-devel':
            fapp.config.from_object('instance.config.LocalDevelConfig')
        elif fapp.config['ENV'] == 'development':
            fapp.config.from_object('instance.config.DevelConfig')
        else:
            fapp.config.from_object('instance.config.ProductionConfig')
    else:
        # load the test config if passed in
        fapp.config.update(test_config)

    logging.config.fileConfig(os.path.join(fapp.instance_path, 'logging.conf'))

    # register the database commands
    from app import database
    database.init_app(fapp)

    # apply the blueprints to the app
    from app import main, wx_auth, user, question, answer, comment, page
    fapp.register_blueprint(main.bp, url_prefix='/')
    fapp.register_blueprint(wx_auth.bp, url_prefix='/auth')
    fapp.register_blueprint(user.bp, url_prefix='/user')
    fapp.register_blueprint(question.bp, url_prefix='/question')
    fapp.register_blueprint(answer.bp, url_prefix='/answer')
    fapp.register_blueprint(comment.bp, url_prefix='/comment')
    fapp.register_blueprint(page.bp, url_prefix='/page')

    # admin
    # set optional bootswatch theme
    from app.database import db, User, Question, Answer, Comment
    from flask_admin import Admin
    from flask_admin.contrib import sqla

    # basic auth
    from flask_basicauth import BasicAuth
    basic_auth = BasicAuth(fapp)

    class ModelView(sqla.ModelView):
        def is_accessible(self):
            if not basic_auth.authenticate():
                raise AuthException('Not authenticated. Refresh the page.')
            else:
                return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(basic_auth.challenge())

    admin = Admin(fapp, name='Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session, endpoint='table_user'))
    admin.add_view(ModelView(Question, db.session, endpoint='table_question'))
    admin.add_view(ModelView(Answer, db.session, endpoint='table_answer'))
    admin.add_view(ModelView(Comment, db.session, endpoint='table_comment'))

    return fapp


def get_logger():
    flask_env = os.getenv('FLASK_ENV')
    if flask_env == 'local-devel':
        return logging.getLogger('wxforum_devel')
    elif flask_env == 'development':
        return logging.getLogger('wxforum_devel')
    return logging.getLogger('wxforum')
