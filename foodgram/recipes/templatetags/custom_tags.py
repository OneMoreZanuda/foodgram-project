from django import template
from urllib.parse import urlencode


register = template.Library()


@register.simple_tag
def field_with_additional_attrs(field, *_, **kwargs):
    attrs = field.field.widget.attrs.copy()
    attrs.update(kwargs)
    return field.as_widget(attrs=attrs)


# @register.filter
# def add_class(field, css):
#     attrs = field.field.widget.attrs.copy()
#     attrs["class"] = css
#     return field.as_widget(attrs=attrs)


# @register.filter
# def update_id(field, new_id):
#     attrs = field.field.widget.attrs.copy()
#     attrs["id"] = new_id
#     return field.as_widget(attrs=attrs)


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