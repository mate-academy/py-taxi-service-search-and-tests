from django import template

register = template.Library()


@register.simple_tag
def update_query_params(request, **kwargs) -> str:
    updated_params = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated_params[key] = value
        else:
            updated_params.pop(key, None)
    return updated_params.urlencode()
