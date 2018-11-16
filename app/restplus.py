import logging
from flask_restplus import Api, cors
from flask import current_app, url_for, render_template


log = logging.getLogger(__name__)

api = Api(version='1.0', title='Automotora Florencia Web Page',
          description='Esta api contiene solo un endpoint para el email de contacto')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not current_app.config['DEBUG']:
        return {'message': message}, 500


@api.documentation
@cors.crossdomain(origin='*')
def custom_ui():
    specs_path = url_for(api.endpoint('specs'))
    return render_template('swagger-ui.html', title=api.title,
                           specs_url=specs_path)
