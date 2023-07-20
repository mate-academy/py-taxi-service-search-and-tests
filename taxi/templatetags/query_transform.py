from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def query_transform(request: HttpRequest, **kwargs):
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            updated[key] = value
        else:
            updated.pop(key, 0)
    print(type(updated.urlencode()))
    return updated.urlencode()
