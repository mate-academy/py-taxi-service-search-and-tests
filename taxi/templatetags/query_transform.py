from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag
def update_query_params(request: HttpRequest, **kwargs) -> str:
    updated_params = request.GET.copy()

    for key, value in kwargs.items():
        if value is not None:
            updated_params[key] = value
        else:
            updated_params.pop(key, None)
    return updated_params.urlencode()
