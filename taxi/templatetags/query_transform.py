from django import template
from django.template.context_processors import request

register = template.Library()


@register.simple_tag
def query_transform(queryset, **kwargs):
    updated = request.Get.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, 0)
    return updated.urlencode()