from django.core.mail import send_mail
from coolsite.celery import app

from .service import send, get_user_text
from .models import *


@app.task
def send_spam_email(user_email):
    send(user_email)

@app.task
def send_user_text(user_text):
    get_user_text(user_text)