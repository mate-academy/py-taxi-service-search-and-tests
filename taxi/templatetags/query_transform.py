from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for kk, vv in kwargs.items():
        if vv is None:
            updated.pop(kk, None)
        else:
            updated[kk] = vv
    return updated.urlencode()
