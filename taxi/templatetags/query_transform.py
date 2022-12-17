from django import template

register = template.Library()


@register.simple_tag()
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for Qk, Qv in kwargs.items():
        if Qv is not None:
            updated[Qk] = Qv
        else:
            updated.pop(Qk, 0)

    return updated.urlencode()
