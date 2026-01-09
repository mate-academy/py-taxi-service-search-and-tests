from django import template


register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    new_request = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            new_request[key] = value
        else:
            new_request.pop(key, 0)
    return new_request.urlencode()
