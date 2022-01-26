from urllib.parse import urlsplit, urlunsplit
from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def url_add_query(url, **kwargs):
    parsed = urlsplit(url)
    querystring = QueryDict(parsed.query, mutable=True)
    querystring.update(kwargs)
    return urlunsplit(parsed._replace(query=querystring.urlencode()))
