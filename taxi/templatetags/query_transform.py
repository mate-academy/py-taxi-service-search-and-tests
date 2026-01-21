from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    params = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            params[key] = value
        else:
            params.pop(key, None)
    return params.urlencode()
