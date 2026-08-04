from django import template


register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    form = request.GET.copy()
    for key, value in kwargs.items():
        if value:
            form[key] = value
        else:
            form.pop(key)
    return form.urlencode()
