from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, val_ in kwargs.items():
        if val_ is not None:
            updated[key] = val_
        else:
            updated.pop(key, 0)
    return updated.urlencode()
