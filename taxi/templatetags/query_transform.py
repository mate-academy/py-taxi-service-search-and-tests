from django import template


register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    new_query = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            new_query[key] = value
        else:
            new_query.pop(key, 0)

    return new_query.urlencode()
