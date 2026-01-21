from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **updates):
    updated_query_params = request.GET.copy()
    for key, value in updates.items():
        if value is not None:
            updated_query_params[key] = value
        else:
            updated_query_params.pop(key, None)
    return updated_query_params.urlencode()
