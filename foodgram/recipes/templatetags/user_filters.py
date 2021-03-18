from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag
def updated_params(dict_, operation, **kwargs):
    dict_copy = dict_.copy()
    if operation == 'update':
        dict_copy.update(kwargs)
    elif operation == 'remove':
        for key in kwargs:
            dict_copy.pop(kwargs, '')
    return urlencode(dict_copy)
