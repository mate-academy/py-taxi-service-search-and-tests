from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated_params = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated_params[key] = value
        else:
            updated_params.pop(key, 0)
    return updated_params.urlencode()
