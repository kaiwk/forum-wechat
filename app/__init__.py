import os
import logging
import logging.config

from flask import Flask

def create_app(test_config=None):
    """
    Create and configure an instance of the Flask application.

    Some config variable we need to specify in 'instance/config.py'

    DEBUG
    SECRET_KEY
    GITHUB_SECRET
    REPO_PATH
    """
    flask = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(flask.instance_path)
    except OSError:
        pass

    # a default secret that should be overridden by instance config
    flask.config.from_mapping(
        SECRET_KEY='this-is-a-secret-key'
    )

    if test_config is None:
        if flask.config['ENV'] == 'local-devel':
            flask.config.from_object('instance.config.LocalDevelConfig')
        elif flask.config['ENV'] == 'development':
            flask.config.from_object('instance.config.DevelConfig')
        else:
            flask.config.from_object('instance.config.ProductionConfig')
    else:
        # load the test config if passed in
        flask.config.update(test_config)

    logging.config.fileConfig(os.path.join(flask.instance_path, 'logging.conf'))

    # register the database commands
    from app import database
    database.init_app(flask)

    # apply the blueprints to the app
    from app import main, wx_auth
    flask.register_blueprint(main.bp, url_prefix='/')
    flask.register_blueprint(wx_auth.bp, url_prefix='/auth')

    return flask


def get_logger():
    if os.getenv('FLASK_ENV') == 'development':
        return logging.getLogger('wxforum_devel')
    return logging.getLogger('wxforum')
