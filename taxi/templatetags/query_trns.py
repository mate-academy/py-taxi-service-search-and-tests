from django import template

register = template.Library()


@register.simple_tag
def query_trns(request, **kwargs):
    updated = request.GET.copy()
    for kv, va in kwargs.items():
        if va is not None:
            updated[kv] = va
        else:
            updated.pop(kv, 0)
    return updated.urlencode()
