from django import template
from django.db.models.sql import Query

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs) -> Query:
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, 0)

    return updated.urlencode()
