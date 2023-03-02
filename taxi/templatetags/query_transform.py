from django import template


register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():  # noqa: VNE001
        if k is not None:  # noqa: VNE001
            updated[k] = v
        else:
            updated.pop(k, 0)

    return updated.urlencode()
