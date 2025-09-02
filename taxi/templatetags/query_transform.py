from django import template

register = template.Library()

@register.simple_tag()
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for key, item in kwargs.items():
        if item is not None:
            updated[key] = item
        else:
            updated.pop(key,0)
    return updated.urlencode()
