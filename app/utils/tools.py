from app.utils import mail
from flask import current_app
from flask_mail import Message


def send_email(username, email, body):
    try:
        msg_body = "El cliente {0}, ha escrito lo siguiente:" \
                   "<br><br> " \
                   "{1} <br><br>  " \
                   "El email de contacto del cliente es: {2}".format(username, body, email)

        msj = Message("Nuevo mensaje página web", sender=("Cliente desde página Web",
                                                          current_app.config['MAIL_USERNAME']))
        msj.html = msg_body
        msj.add_recipient(current_app.config['MAIL_RECIPIENT'])
        mail.send(msj)
        return True
    except Exception as e:
        print("ERROR: {0}".format(e))
        return False