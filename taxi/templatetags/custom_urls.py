from django import template

register = template.Library()


@register.simple_tag
def custom_urls(request, **kwargs):
    filters = request.GET.copy()
    filters.update(kwargs)
    return filters.urlencode()
