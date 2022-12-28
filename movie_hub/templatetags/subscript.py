from django import template

register = template.Library()

@register.filter(name='subscript')
def subscript(obj, attribute):
    return obj[attribute]
