from django import template
import calendar

register = template.Library()

@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]

@register.filter(name='lookup')
def lookup(d, key):
    return d[key]


@register.filter
def quote_rep(value):
    value = str(value)
    return value.replace("'",'"')

@register.filter
def index(List, i):
    return List[int(i)]