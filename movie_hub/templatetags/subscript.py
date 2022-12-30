from django import template

register = template.Library()

@register.filter(name='subscript')
def subscript(obj, attribute):
    val = getattr(obj, attribute, None)
    if val: 
        return val
    else:
        return obj[attribute]
