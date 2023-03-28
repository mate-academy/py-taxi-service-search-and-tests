from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    update = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            update[key] = value
        else:
            update.pop(key, 0)

    return update.urlencode()
