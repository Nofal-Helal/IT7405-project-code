from django import template

register = template.Library()


@register.filter(name='num_k_m', is_safe=False)
def num_k_m(val, precision=2):

    try:
        int_val = int(val)
    except ValueError:
        raise template.TemplateSyntaxError(
            f'Value must be an integer. {val} is not an integer')

    if int_val < 1000:
        return str(int_val)
    elif int_val < 1_000_000:
        return f'{ int_val/1000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'K'
    else:
        return f'{int_val/1_000_000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'M'
