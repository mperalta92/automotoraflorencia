import logging
from flask import request, jsonify, redirect, url_for
from app.restplus import api
from flask_restplus import Resource, cors
from app.utils.serializers import email_args
from app.utils.tools import send_email

log = logging.getLogger(__name__)

ns = api.namespace('email', description='manage clients emails')


@ns.route('/')
class InboxEmail(Resource):

    @api.expect(email_args)
    @cors.crossdomain(origin='*')
    def post(self):
        '''

        return 200 if en email was sent to user
        '''

        args = request.args
        client_username = args.get('name')
        client_message = args.get('message')
        client_email = args.get('email')

        try:
            status = send_email(client_username, client_email, client_message)
            response_message = "Email was sending successfully" if status else "Email wasn't sending correctly :("
            response_code = 200 if status else 400

            response = jsonify({"msg": response_message, "code": 200})
            response.status_code = response_code

            return redirect('/')
        except Exception as err:
            logging.error(err)
            response_message = "Email wasn't sending correctly :("
            response_code = 500
            response = jsonify({"msg": response_message, "error": str(err), "code": 500})
            response.status_code = response_code
