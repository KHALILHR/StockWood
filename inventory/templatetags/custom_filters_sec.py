from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    # Convert the value to a string and split into integer and decimal parts
    parts = str(value).split('.')
    
    # Check if the integer part is not an empty string before conversion
    if parts[0]:
        # Add a space as a thousands separator for the integer part
        integer_part = "{:,}".format(int(parts[0])).replace(",", " ")
    else:
        integer_part = "0"

    # Join the formatted integer part with the decimal part
    if len(parts) == 1:
        return integer_part
    else:
        return f"{integer_part}.{parts[1]}"

