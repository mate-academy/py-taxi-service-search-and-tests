from django import template

register = template.Library()


@register.simple_tag
def paginate_url(request, page):
    params = request.GET.copy()
    params["page"] = page
    return "?" + params.urlencode()
