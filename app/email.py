from flask import render_template, app as current_app
from flask_mail import Message

from . import mail


def mail_message(subject, template, to, **kwargs):
    sender_email = current_app.config['SENDER_MAIL_USERNAME']

    email = Message(subject, sender=sender_email, recipients=[to])
    email.body = render_template(template + ".txt", **kwargs)
    email.html = render_template(template + ".html", **kwargs)
    mail.send(email)
