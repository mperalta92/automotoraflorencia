from app.restplus import api
from flask_restplus import fields

email_args = api.model('email_args', {
    'username': fields.String(required=True, description='username'),
    'body': fields.String(required=True, description='body'),
    'email': fields.String(required=True, description='email')
})