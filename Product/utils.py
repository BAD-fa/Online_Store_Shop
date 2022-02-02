import json

from django.contrib.auth.models import AnonymousUser
from django.core.cache import caches
from django.db.models import Q

from .models import Product



def add_to_cart(request, product):
    redis_cache = caches['default']
    redis_client = redis_cache.client.get_client()
    if not isinstance(request.user, AnonymousUser):
        redis_client.hset(request.user.email, mapping=product)
    else:
        redis_client.hset(request.session.session_key, mapping=product)


def dict_decoder(binary_dict):
    data = {}
    for k, v in binary_dict.items():
        data[k.decode("utf-8")] = json.loads(v)
    return data


def params_creator(request):
    properties = request.GET.getlist('property')
    details = request.GET.getlist('detail')
    if properties and details:
        query = Q(property=properties[0])
        query |= Q(detail=details[0])

        for p, d in zip(properties[1:], details[1:]):
            query |= Q(property=p)
            query |= Q(detail=d)
    else:
        query = Q()

    qs = Product.objects.all()
    filtered_qs = Product.objects.none()
    for p in qs:
        det = p.details.filter(query)
        if det:
            filtered_qs |= p

    return query
