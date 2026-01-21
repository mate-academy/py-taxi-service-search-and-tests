from django import template
from django.http import HttpResponse, HttpRequest
register = template.Library()


@register.simple_tag
def query_transform(request: HttpRequest, **kwargs) -> HttpResponse:
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, 0)
    return updated.urlencode()
