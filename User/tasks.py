from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task

from .utils import account_activation_token

@shared_task
def email_text_genrator_sender(request,user,template,to_email,mail_subject):
        current_site = get_current_site(request)
        message = render_to_string(f'{template}', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])