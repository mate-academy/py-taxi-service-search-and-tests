from django.template import Library


register = Library()


@register.simple_tag
def query_transform(request, **kwargs):
    query_params = request.GET.copy()
    for key, value in kwargs.items():
        query_params[key] = value
    return query_params.urlencode()
