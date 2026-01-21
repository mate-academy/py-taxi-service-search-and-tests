from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for kay, value in kwargs.items():
        if value is not None:
            updated[kay] = value
        else:
            updated.pop(kay, 0)
    return updated.urlencode()
