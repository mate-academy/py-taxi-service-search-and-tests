from django import template
from django.http import HttpRequest
from typing import Any

register = template.Library()


@register.simple_tag
def query_transform(
        request: HttpRequest,
        **kwargs: Any
) -> str:
    update = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            update[key] = value
        else:
            update.pop(key, 0)
    return update.urlencode()
