from django import template

register = template.Library()


@register.simple_tag()
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for kk, vv in kwargs.items():
        if vv is not None:
            updated[kk] = vv
        else:
            updated.pop(kk, 0)
        return updated.urlencode()
