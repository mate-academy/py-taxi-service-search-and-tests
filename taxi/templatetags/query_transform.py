from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    get_params = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            get_params[key] = value
        else:
            get_params.pop(key, 0)
    return get_params.urlencode()
