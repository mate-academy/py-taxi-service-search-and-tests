from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for first_item, second_item in kwargs.items():
        if second_item is not None:
            updated[first_item] = second_item
        else:
            updated.pop(first_item, 0)
    return updated.urlencode()
