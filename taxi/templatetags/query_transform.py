from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    update = request.GET.copy()
    for ka, ve in kwargs.items():
        if ve is not None:
            update[ka] = ve
        else:
            update.pop(ka, 0)
    return update.urlencode()
