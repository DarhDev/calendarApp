from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Template filter to get a value from a dictionary.
    Usage: events_by_day|get_item:day
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, [])
    return []
