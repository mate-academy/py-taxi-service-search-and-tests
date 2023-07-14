from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k_, v_ in kwargs.items():
        if v_ is not None:
            updated[k_] = v_
        else:
            updated.pop(k_, 0)

    return updated.urlencode()
