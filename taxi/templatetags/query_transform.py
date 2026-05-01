from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k_var, v_var in kwargs.items():
        if v_var is not None:
            updated[k_var] = v_var
        else:
            updated.pop(k_var, 0)
    return updated.urlencode()
