import os
import random

import redis
from random import randint
from decouple import config
import requests
from django.conf import settings
from django.core.mail import send_mail

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def generate_code():
    return randint(100000, 999999)


def send_code(email):
    if redis_connection.get(email):
        return False, "Code already sent"

    code = generate_code()
    send_email_code(email, code)
    print(f"Your code for  {email} is {code}")

    redis_connection.set(email, code)
    redis_connection.expire(email, time=120)

    return True, "Code sent successfully"


def verify_code_cache(email, code):
    data = redis_connection.get(email)
    if not data:
        return False, "Code expired"
    stored_code = data.decode('utf-8')
    if stored_code == code:
        redis_connection.set(f"{email}_verified", "True")
        redis_connection.expire(f"{email}_verified", time=120)
        return True, "Code verified successfully"
    return False, "Code is incorrect"


def check_verification_status(email):
    verified_phone = redis_connection.get(f"{email}_verified")
    if not verified_phone:
        return False, "Email must be verified first"
    if verified_phone.decode('utf-8') != "True":
        return False, "Email is not verified"
    return True, "Email is verified"


def send_email_code(email, code):
    subject = 'Your verification code'
    message = f'Your verification code is {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
