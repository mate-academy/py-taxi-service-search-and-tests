from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def url_query_params_concatenation(request: HttpRequest, **kwargs) -> str:
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, None)

    return updated.urlencode()
