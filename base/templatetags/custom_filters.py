from django import template
from django.utils.safestring import mark_safe

register = template.Library()




@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter()
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.filter()
def placeholder(value):
    """
    Render a muted placeholder if value equates to False.
    """
    if value:
        return value
    placeholder = '<span class="text-muted">&mdash;</span>'
    return mark_safe(placeholder)


@register.simple_tag
def field_verbose_name(value, field):
    '''
    Django template filter which returns 
    the verbose name of an field from a model.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.get_field(field).verbose_name.title()


