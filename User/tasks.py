from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def email_sender(message, to_email, mail_subject):
    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
