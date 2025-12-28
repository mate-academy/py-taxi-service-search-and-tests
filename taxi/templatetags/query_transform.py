from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def query_transform(request: HttpRequest, **kwargs) -> str:
    updated = request.GET.copy()
    for param, value in kwargs.items():
        if value is not None:
            updated[param] = value
        else:
            updated.pop(param, 0)
    return updated.urlencode()
