from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for ki, vi in kwargs.items():
        if vi is not None:
            updated[ki] = vi
        else:
            updated.pop(ki, 0)

    return updated.urlencode()
