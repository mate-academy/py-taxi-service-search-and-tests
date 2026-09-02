from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k_1, v_1 in kwargs.items():
        if v_1 is not None:
            updated[k_1] = v_1
        else:
            updated.pop(k_1, 0)
    return updated.urlencode()
