from django import template
register = template.Library()


@register.simple_tag
def field_with_additional_attrs(field, *_, **kwargs):
    attrs = field.field.widget.attrs.copy()
    attrs.update(kwargs)
    return field.as_widget(attrs=attrs)
