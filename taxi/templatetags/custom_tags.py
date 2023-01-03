from django import template

register = template.Library()


@register.simple_tag
def url_params(request, **kwargs):
    params = request.GET.copy()

    for key, value in kwargs.items():
        if value:
            params[key] = value
        else:
            params.pop(key)

    if len(params):
        return "?" + params.urlencode()

    return None
