from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for kov, vok in kwargs.items():
        if vok is not None:
            updated[kov] = vok
        else:
            updated.pop(kov, 0)
    return updated.urlencode()
