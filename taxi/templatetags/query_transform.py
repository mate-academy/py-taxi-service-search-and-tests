from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    print("request.GET", request.GET)
    print("kwargs", kwargs)
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)
    return updated.urlencode()
