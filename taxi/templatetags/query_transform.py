from django import template

register = template.Library()


@register.simple_tag
def query_transform(req, **kwargs):
    updates = req.GET.copy()

    for key, value in kwargs.items():
        if value:
            updates[key] = value
        else:
            updates.pop(key, 0)

    return updates.urlencode()
