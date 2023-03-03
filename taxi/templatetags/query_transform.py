from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for page, value in kwargs.items():
        if value is not None:
            updated[page] = value
        else:
            updated.pop(page, 0)
    return updated.urlencode()
