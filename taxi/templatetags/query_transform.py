from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for item, value in kwargs.items():
        if value is not None:
            updated[item] = value
        else:
            updated.pop(item, 0)
    return updated.urlencode()
