from django import template
import locale

register = template.Library()

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

@register.filter(name='truncate_chars')
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value

@register.filter
def format_currency(value):
    try:
        # Konvertiere den Wert in eine Float-Zahl und formatiere sie
        value = float(value)
        return locale.format_string("%.2f", value, grouping=True)
    except (ValueError, TypeError):
        return value

@register.filter
def format_length(value):
    try:
        # Konvertiere den Wert in eine Float-Zahl und formatiere sie
        value = float(value)
        return locale.format_string("%.2f", value, grouping=True)
    except (ValueError, TypeError):
        return value

