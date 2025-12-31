from django.http import HttpRequest
from django import template


register = template.Library()


@register.simple_tag
def query_transform(request: HttpRequest, **kwargs) -> str:
    updated_request = request.GET.copy()

    for key, value in kwargs.items():
        if value is not None:
            updated_request[key] = value
        else:
            updated_request.pop(key, 0)

    return updated_request.urlencode()
