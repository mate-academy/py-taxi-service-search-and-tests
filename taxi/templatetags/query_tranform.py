from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for parameter, value in kwargs.items():
        if value is not None:
            updated[parameter] = value
        else:
            updated.pop(parameter, 0)
    return updated.urlencode()
