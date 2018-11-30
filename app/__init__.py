import os

from flask import Flask

from app import weixin_logger

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
        if flask.config['ENV'] == 'development':
            flask.config.from_object('instance.config.DevelConfig')
        else:
            flask.config.from_object('instance.config.ProductionConfig')
    else:
        # load the test config if passed in
        flask.config.update(test_config)

    # register the database commands
    from app import database
    database.init_app(flask)

    # apply the blueprints to the app
    from app import main
    flask.register_blueprint(main.bp, url_prefix='/')

    return flask
