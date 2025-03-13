from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated_query = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated_query[key] = value
        else:
            updated_query.pop(key, None)
    return updated_query.urlencode()
