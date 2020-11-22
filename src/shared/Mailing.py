import os
from flask import Flask, render_template
from flask_mail import Message
from ..app import mail


app = Flask(__name__)

class Mailing():
    """
    Mail Class
    """
    @staticmethod
    def send_mail(user):
        try:
            app.logger.info('llego la funcion    '+user.email)
            msg = Message("[CONECTIKA:TECH] Correo prueba",
            sender="app@conectika.tech",
            recipients=[user.email])
            msg.body = 'Hola '+user.name+',\n esto es un correo con FLASK porque creaste un nuevo blog'
            msg.html = render_template('email_template.html', name=user.name)
            mail.send(msg)
        except Exception as e:
            app.logger.error(e)
            raise Exception(e)