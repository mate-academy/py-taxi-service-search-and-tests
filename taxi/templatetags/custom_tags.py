from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    query = request.GET.copy()

    for key, value in kwargs.items():
        if value:
            query[key] = value
        else:
            query.pop(key)

    return query.urlencode()
