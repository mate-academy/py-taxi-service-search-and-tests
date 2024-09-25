from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, values in kwargs.items():
        if values is not None:
            updated[key] = values
        else:
            updated.pop(key, 0)
    return updated.urlencode()
