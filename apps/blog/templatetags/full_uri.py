from django.template.defaultfilters import register


@register.filter
def full_uri(value, request):
    return request.build_absolute_uri('/')[:-1] + value
