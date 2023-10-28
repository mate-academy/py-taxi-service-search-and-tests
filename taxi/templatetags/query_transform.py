from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for first, second in kwargs.items():
        if second is not None:
            updated[first] = second
        else:
            updated.pop(first, 0)
    return updated.urlencode()
