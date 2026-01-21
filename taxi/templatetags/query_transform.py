from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated_query_params = request.GET.copy()
    for param_name, param_value in kwargs.items():
        if param_value is not None:
            updated_query_params[param_name] = param_value
        else:
            updated_query_params.pop(param_name, 0)
    return updated_query_params.urlencode()
