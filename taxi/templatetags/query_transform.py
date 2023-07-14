from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for index, value in kwargs.items():
        if value is not None:
            updated[index] = value
        else:
            updated.pop(index, 0)

        return updated.urlencode()
