from flask import Flask
__author__ = 'talamo_a'
from config import Config


def create_core():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    if Config.TYPE == 'tcp' or Config.type == 'unix':
        with app.app_context():
            from . import routes  # Import routes
            return app

    else:
        raise SystemExit('Unsupported docker socket type ' + Config.type)
