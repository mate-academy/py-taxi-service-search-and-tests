from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated_params = request.GET.copy()

    for key, value in kwargs.items():
        if value is None:
            updated_params.pop(key, None)
        else:
            updated_params[key] = value

    return updated_params.urlencode()
