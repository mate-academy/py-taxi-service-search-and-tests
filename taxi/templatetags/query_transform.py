from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    query_params = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            query_params[key] = value
        else:
            query_params.pop(key, None)
    return query_params.urlencode()
