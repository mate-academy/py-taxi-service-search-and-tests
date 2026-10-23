from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    """Return the current query string with the given parameters replaced.

    Pagination links use it to change only ``page`` and keep the search
    query, e.g. ``?model=ford&page=2``. A parameter passed as ``None`` is
    removed.
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is None:
            updated.pop(key, None)
        else:
            updated[key] = value
    return updated.urlencode()
