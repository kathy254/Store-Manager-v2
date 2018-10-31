from flask import Flask

from .api.v2 import app_v2
from instance.config import app_config


def create_app(config):
    app = Flask(__name__)
    app.register_blueprint(app_v2)
    app.config.from_object(app_config[config])
    return app