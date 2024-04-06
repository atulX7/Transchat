import logging
import os
from datetime import timedelta
from random import choice

from dotenv import load_dotenv
from flask import (
    Flask,
    g,
    session,
)

from flask_login import LoginManager, current_user
from werkzeug.middleware.proxy_fix import ProxyFix

from .blueprints import discover_blueprints
from .mixin import User
from .services import OpenAIHelper, _session_logout, _session_login
from .utils import log_setup


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv(
        "FLASK_SECRET_KEY",
        "".join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for i in range(20)]),
    )
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['OUTPUT_FOLDER'] = 'output'

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])

    # session will expire after PERMANENT_SESSION_LIFETIME
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
    log_setup(app)

    # The following is required to run on ECS or any other host with reverse proxy:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    app.config["TEMPLATES_AUTO_RELOAD"] = True

#    app.login_manager = LoginManager(app)
    load_configs(app)
    register_blueprints(app)

    app.openai = OpenAIHelper()
    return app


def load_configs(app: Flask):
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        parent_dir = os.path.dirname(basedir)
        load_dotenv(os.path.join(parent_dir, ".env"))
    except Exception as e:
        logging.error(e)


def register_blueprints(app: Flask):
    for blueprint in discover_blueprints():
        app.register_blueprint(blueprint)
