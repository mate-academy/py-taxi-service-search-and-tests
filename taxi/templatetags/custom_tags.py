from django import template

register = template.Library()


@register.inclusion_tag("taxi/search_form.html")
def search(search_by, search_object):
    return {
        "search_by": search_by,
        "search_object": search_object
    }
