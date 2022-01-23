from django.contrib.auth.models import AnonymousUser
from django.core.cache import caches

from .utils import dict_decoder


def cart(request):
    redis_cache = caches['default']
    redis_client = redis_cache.client.get_client()

    if not isinstance(request.user, AnonymousUser):

        binary_data = redis_client.hgetall(request.user.email)
        return {"cart": dict_decoder(binary_data)}

    else:

        binary_data = redis_client.hgetall(request.session.session_key)
        return {"cart": dict_decoder(binary_data)}
