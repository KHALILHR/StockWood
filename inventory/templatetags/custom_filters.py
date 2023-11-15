from django import template

register = template.Library()

@register.filter
def calculate_total_quantity(stock_list):
    return sum(stock.quantity for stock in stock_list)

