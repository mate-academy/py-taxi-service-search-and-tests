from django import template
from django.db.models.sql import Query

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs) -> Query:
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)

    return updated.urlencode()
