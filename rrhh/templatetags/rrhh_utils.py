from django import template

register = template.Library()

months = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}


@register.filter
def beauty_none(value):
    if value is None or value == '':
        return 'No especificado'
    else:
        return value


@register.filter
def start_with(value, arg):
    return value.startswith(arg)


@register.filter
def end_with(value, arg):
    return True if value.endswith(arg) else False


@register.filter
def get_word(value, arg):
    return value.split(' ')[int(arg) - 1]


@register.filter
def get_real_month(value):
    return months[value]


@register.filter
def encrypt_phrase_for_url(value):
    return value.replace(' ', '_')


@register.filter
def decrypt_phrase_from_url(value):
    return value.replace('_', ' ')
