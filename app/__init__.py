from flask import Flask

from .api.v2 import app_v2
from instance.config import app_config
from manage import DbSetup

config_name = 'development'

db = DbSetup(config_name)

def create_app(config):
    #this is where we configure our flask app
    app = Flask(__name__)
    db.db_tables()
    app.register_blueprint(app_v2)
    app.config.from_object(app_config[config])
    app.config['testing'] = True
    return app