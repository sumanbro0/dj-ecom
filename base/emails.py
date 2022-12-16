from django.conf import settings
from django.core.mail import send_mail


def send_account_activation_email(email, email_token):

    subject = "Your account needs to be verified"
    email_from = settings.EMAIL_HOST_USER
    message = f"Hi, click on the link to activate your account {settings.DEFAULT_DOMAIN}/accounts/activate/{email_token}/"
    send_mail(subject, message, email_from, [email])


def send_change_password_email(email, uid):
    subject = "Your account needs to be verified"
    email_from = settings.EMAIL_HOST_USER
    message = f"Hi, click on the link to change your password {settings.DEFAULT_DOMAIN}/accounts/change_pwd/{uid}/"
    # message = f"Hi, click on the link to change your password 127.0.0.1:8000/change_pwd/{uid}/"
    send_mail(subject, message, email_from, [email])
