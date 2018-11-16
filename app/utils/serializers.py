from flask_restplus import reqparse

email_args= reqparse.RequestParser()
email_args.add_argument('name', type=str, required=True, help='name')
email_args.add_argument('message', type=str, required=True, help='message')
email_args.add_argument('email', type=str, required=True, help='email')
