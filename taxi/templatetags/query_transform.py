from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for kwarg, value in kwargs.items():
        if value is not None:
            updated[kwarg] = value
        else:
            updated.pop(kwarg, 0)
    return updated.urlencode()
