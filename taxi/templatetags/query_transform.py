from django import template


register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, vey in kwargs.items():
        if vey is not None:
            updated[key] = vey
        else:
            updated.pop(key, 0)
    return updated.urlencode()
