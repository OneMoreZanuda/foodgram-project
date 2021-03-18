from django import template
from urllib.parse import urlencode

register = template.Library()


@register.inclusion_tag("includes/tag_item.html", takes_context=True)
def tag_item(context):
    name = context['name']
    checked = context[name]

    query_params = context['request'].GET
    new_query_params = query_params.copy()
    new_query_params.pop(name, '')
    if checked:
        new_query_params[name] = 'no'
        
    new_query_string = urlencode(new_query_params)
    link = './' if new_query_string else f'?{new_query_string}'

    return {
        'name': name,
        'checked': checked,
        'link': link,
        'label': context['label'],
        'color': context['color']
    }
