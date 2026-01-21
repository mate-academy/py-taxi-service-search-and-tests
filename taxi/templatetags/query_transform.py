from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    update = request.GET.copy()
    for first_ag, second_ag in kwargs.items():
        if second_ag is not None:
            update[first_ag] = second_ag
        else:
            update.pop(first_ag)
    return update.urlencode()
