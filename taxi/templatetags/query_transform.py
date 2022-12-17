from django import template

register = template.Library()


@register.simple_tag()
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for queryk, queryv in kwargs.items():
        if queryv is not None:
            updated[queryk] = queryv
        else:
            updated.pop(queryk, 0)

    return updated.urlencode()
