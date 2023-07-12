from django import template

register = template.Library()


@register.simple_tag()
def query_transform(request, **kwargs):
    updated = request.GET.copy()

    for ka, ve in kwargs.items():
        if ve is not None:
            updated[ka] = ve
        else:
            updated.pop(ka, 0)

    return updated.urlencode()
