from django.core.mail import send_mail
from coolsite.celery import app

from .service import send
from .models import *


@app.task
def send_spam_email(user_email):
    send(user_email)