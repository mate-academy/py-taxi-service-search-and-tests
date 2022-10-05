from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    update = request.GET.copy()

    for k, v in kwargs.items():
        if v:
            update[k] = v
        else:
            update.pop(k, 0)
    return update.urlencode()
