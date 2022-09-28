from django import template

register = template.Library()


@register.simple_tag
def search_transform(request, **kwargs):
    request_copy = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            request_copy[key] = value
        else:
            request_copy.pop(key, 0)

    return request_copy.urlencode()
