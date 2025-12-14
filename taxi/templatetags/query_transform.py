from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    query = request.GET.copy()

    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()
