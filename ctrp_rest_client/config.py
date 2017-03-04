from flask import config
import os


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '2z54e22a-1r39-1525-b42a-t49cw3au7f5b'
    BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = False


config = {
    "development": "ctrp_rest_client.config.DevelopmentConfig",
    "testing": "ctrp_rest_client.config.TestingConfig",
    "default": "ctrp_rest_client.config.BaseConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)