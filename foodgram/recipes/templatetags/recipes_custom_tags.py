from django import template
from urllib.parse import urlencode


register = template.Library()


@register.simple_tag
def field_with_additional_attrs(field, *_, **kwargs):
    attrs = field.field.widget.attrs.copy()
    attrs.update(kwargs)
    return field.as_widget(attrs=attrs)


@register.inclusion_tag("recipes/includes/tag_item.html", takes_context=True)
def tag_item(context):
    tag = context['tag']
    redirect_request_params = context['request'].GET.copy()
    redirect_request_params.pop(tag.name, None)

    # return to the first page when changing tags
    redirect_request_params.pop('page', None)

    if tag.checked:
        redirect_request_params[tag.name] = 'no'

    query_string = urlencode(redirect_request_params)
    link = f'?{query_string}' if query_string else './'

    return {
        'tag': tag,
        'link': link,
    }


@register.filter
def exclude_item(dict_, key):
    dict_copy = dict_.copy()
    dict_copy.pop(key, None)
    return dict_copy


@register.filter
def add_correct_recipe_word_form(count):
    rest100 = count % 100
    if rest100 in range(11, 15):
        return f'{count} рецептов'

    rest10 = count % 10
    if rest10 == 1:
        return f'{count} рецепт'
    elif rest10 in range(2, 5):
        return f'{count} рецепта'
    else:
        return f'{count} рецептов'
