from django import template


register = template.Library()


@register.simple_tag()
def query_transform(request, **kwargs):
    update = request.GET.copy()
    for some_key, some_value in kwargs.items():
        if some_value is not None:
            update[some_key] = some_value
        else:
            update.pop(some_key, 0)

    return update.urlencode()
