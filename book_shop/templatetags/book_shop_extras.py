from django import template
from django.template.defaultfilters import stringfilter


@stringfilter
def map_available_tag(value):
    """Removes all values of arg from the given string"""
    if value == "REQ":
        return "по запросу"
    if value == "WARE" or value == "SHOP":
        return "в магазине"
    if value == "NOT":
        return "недоступно"
    return "нераспознанная доступность"


register = template.Library()
register.filter('map_available_tag', map_available_tag)
