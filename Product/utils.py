from django.contrib.auth.models import AnonymousUser
from django.core.cache import caches


def add_to_cart(request, product):
    redis_cache = caches['default']
    redis_client = redis_cache.client.get_client()
    if not isinstance(request.user, AnonymousUser):
        redis_client.hset(request.user.email, mapping=product)
    else:
        redis_client.hset(request.session.session_key, mapping=product)
