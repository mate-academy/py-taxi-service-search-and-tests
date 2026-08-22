from django import template

register = template.Library()


@register.simple_tag()
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for ka, va in kwargs.items():
        if va is not None:
            updated[ka] = va
        else:
            updated.pop(ka, 0)
    return updated.urlencode()
