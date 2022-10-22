from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, val in kwargs.items():
        if val is not None:
            updated[key] = val
        else:
            updated.pop(key, 0)
    return updated.urlencode()
