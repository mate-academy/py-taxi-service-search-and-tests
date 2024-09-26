from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()

    for keys, values in kwargs.items():
        if values is not None:
            updated[keys] = values
        else:
            updated.pop(keys, 0)

    return updated.urlencode()
