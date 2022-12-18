from django import template

register = template.Library()


@register.simple_tag()
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for page, num in kwargs.items():
        if num is not None:
            updated[page] = num
        else:
            updated.pop(page, 0)

    return updated.urlencode()
