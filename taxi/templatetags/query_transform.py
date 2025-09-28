from __future__ import annotations

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs) -> str:
    """
    Build a new querystring preserving existing parameters and
    overriding only the provided keys. Use like:
    href="?{% query_transform page=2 %}"
    """
    request = context["request"]
    query = request.GET.copy()
    for key, value in kwargs.items():
        if value is None:
            query.pop(key, None)
        else:
            query[key] = value
    return query.urlencode()
