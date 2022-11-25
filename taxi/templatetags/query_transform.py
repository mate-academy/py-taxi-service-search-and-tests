from pickle import GET
from typing import Any

from django import template

register = template.Library()


@register.simple_tag
def query_transform(
        request: {GET},
        **kwargs: dict[str, Any],
) -> Any:
    update = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            update[key] = value
        else:
            update.pop(key, 0)

    return update.urlencode()
