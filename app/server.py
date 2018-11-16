import os
from flask import Flask, Blueprint
from flask_compress import Compress
from app.static import resources
from app.utils import bcrypt
from app.utils import mail
from app.restplus import api
from app.endpoints.contact import ns as ns_contact
from werkzeug.contrib.fixers import ProxyFix


def create_app(config=None, logging_config=None):
    """
    Crea la aplicacion
    :param config: path del archivo de configuracion
    """

    app = Flask(
        __name__,
        static_url_path='',
        static_folder="./static",
        template_folder="./static",
    )
    
    if config is None:
        config = os.path.join(os.getcwd(), 'app/config.ini')
    elif os.path.exists(os.path.join(os.getcwd(), config)):
        config = os.path.join(os.getcwd(), config)
    else:
        raise FileExistsError('config.ini not found')
    app.config.from_pyfile(config)

    if not app.config['SHOW_DOCUMENTATION']:
        api._doc = False

    blueprint = Blueprint('app', __name__, url_prefix='/app')
    api.init_app(blueprint)
    api.add_namespace(ns_contact)
    app.register_blueprint(blueprint)
    resources.initialize_app(app)
    bcrypt.init_app(app)
    set_email_params(app)
    mail.init_app(app)
    # TODO: Evaluate Compress utility
    Compress(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app


def set_email_params(app):
    app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME'] if 'MAIL_USERNAME' in os.environ \
        else app.config['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD'] if 'MAIL_PASSWORD' in os.environ \
        else app.config['MAIL_PASSWORD']
    app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER'] if 'MAIL_SERVER' in os.environ \
        else app.config['MAIL_SERVER']
    app.config['MAIL_PORT'] = os.environ['MAIL_PORT'] if 'MAIL_PORT' in os.environ \
        else app.config['MAIL_PORT']

    tls = app.config['MAIL_USE_TLS']
    ssl = app.config['MAIL_USE_SSL']

    if 'MAIL_USE_TLS' in os.environ and os.environ['MAIL_USE_TLS'] == 'False':
        tls = False
    if 'MAIL_USE_TLS' in os.environ and os.environ['MAIL_USE_TLS'] == 'True':
        tls = True

    if 'MAIL_USE_SSL' in os.environ and os.environ['MAIL_USE_SSL'] == 'False':
        ssl = False
    if 'MAIL_USE_SSL' in os.environ and os.environ['MAIL_USE_SSL'] == 'True':
        ssl = True

    app.config['MAIL_USE_TLS'] = tls
    app.config['MAIL_USE_SSL'] = ssl
