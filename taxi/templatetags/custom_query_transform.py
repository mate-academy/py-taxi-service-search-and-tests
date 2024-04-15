from django import template


register = template.Library()


@register.simple_tag
def custom_query_transform(request, **kwargs):
    updated_request = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            updated_request[key] = value
        updated_request.pop(key, 0)
    return updated_request.urlencode()
