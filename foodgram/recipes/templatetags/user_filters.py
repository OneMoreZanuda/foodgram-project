from django import template
from urllib.parse import urlencode


register = template.Library()


@register.inclusion_tag("recipes/includes/tag_item.html", takes_context=True)
def tag_item(context):
    name = context['name']
    checked = context[name]

    query_params = context['request'].GET
    new_query_params = query_params.copy()
    new_query_params.pop(name, None)

    # return to the first page when changing it
    new_query_params.pop('page', None)

    if checked:
        new_query_params[name] = 'no'

    new_query_string = urlencode(new_query_params)
    link = f'?{new_query_string}' if new_query_string else './'

    return {
        'name': name,
        'checked': checked,
        'link': link,
        'label': context['label'],
        'color': context['color']
    }


@register.filter
def exclude_item(dict_, key):
    dict_copy = dict_.copy()
    dict_copy.pop(key, None)
    return dict_copy
