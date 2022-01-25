from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


from User.models import UserDevice

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def user_device(request,user):
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    elif request.user_agent.is_tablet:
        device_type = "Tablet"
    elif request.user_agent.is_pc:
        device_type = "PC"

    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    UserDevice.objects.create(device_type=device_type, browser_type=browser_type, browser_version=browser_version,
                            os_type=os_type, os_version=os_version,user=user,session=request.session.session_key)
