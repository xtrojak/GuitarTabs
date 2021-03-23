from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config
from .libs.templating import create_info_template

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy(session_options={'expire_on_commit': False})
info_template = create_info_template()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .core import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
