from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    update = request.GET.copy()
    for key1, vay2 in kwargs.items():
        if vay2 is not None:
            update[key1] = vay2
        else:
            update.pop(key1)
    return update.urlencode()
