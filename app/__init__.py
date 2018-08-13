from flask import Flask
from flask_jwt import JWT
from conf.config import config
import logging




def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # jwt = JWT(app, authenticate, identity)

    from .rest import rest as rest_blueprint
    app.register_blueprint(rest_blueprint)

    return app