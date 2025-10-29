from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    """
    Keeps existing query parameters and overrides with new ones.
    Useful for pagination links that should preserve search filters.
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        updated[key] = value
    return updated.urlencode()
