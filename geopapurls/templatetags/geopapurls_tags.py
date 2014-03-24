from django import template

register = template.Library()
@register.simple_tag(takes_context=True)
def url_add_query(context, **kwargs):
    request = context.get('request')

    get = request.GET.copy()
    get.update(kwargs)

    path = '%s?' % request.path
    for query, val in get.items():
        path += '%s=%s&' % (query, val)

    return path[:-1]