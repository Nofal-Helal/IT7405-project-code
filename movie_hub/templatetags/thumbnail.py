from django import template
import re

register = template.Library()


@register.filter(name='thumbnail', is_safe=False)
def thumbnail(val, height=620):
    if type(val) != str:
        raise template.TemplateSyntaxError(
            f'Value must be a string. {val} is not a string')

    if val.startswith("https://m.media-amazon"):
        return val[:-4] + '._V1_SY' + str(height) + '_.jpg'
    else:
        return val
