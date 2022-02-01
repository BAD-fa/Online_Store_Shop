from time import time
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


from User.models import UserDevice

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def genrate_user_device(request,user):
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    elif request.user_agent.is_tablet:
        device_type = "Tablet"
    elif request.user_agent.is_pc:
        device_type = "PC"

    os_type = request.user_agent.os.family
    device_brand = request.user_agent.device.family
    check_field = hash(os_type+device_type+device_brand)
    user_device = list(user.device.all().values_list('check_field'))
    if check_field in user_device:
        device = UserDevice.objects.get(check_field=check_field).last_loging = timezone.now()
        device.save()
        return None
    else:
        return UserDevice.objects.create(device_type=device_type,os_type=os_type,user=user,check_field=check_field,device_brand=device_brand)

def email_genrator(request,user,template):
        current_site = get_current_site(request)
        message = render_to_string(f'{template}', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        return message

def token_validator(uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return user
    if user is not None and account_activation_token.check_token(user, token):
        return user