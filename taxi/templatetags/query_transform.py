from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    update = request.GET.copy()
    for key, key_val in kwargs.items():
        if key_val is not None:
            update[key] = key_val
        else:
            update.pop(key, 0)
    return update.urlencode()
