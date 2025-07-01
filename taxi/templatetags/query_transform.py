from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for parameter_name, parameter_value in kwargs.items():
        if parameter_value is not None:
            updated[parameter_name] = parameter_value
        else:
            updated.pop(parameter_name, 0)
    return updated.urlencode()
