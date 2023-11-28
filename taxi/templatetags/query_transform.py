from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()

    for key, variab in kwargs.items():
        if variab is not None:
            updated[key] = variab
        else:
            updated.pop(key, 0)
    return updated.urlencode()
