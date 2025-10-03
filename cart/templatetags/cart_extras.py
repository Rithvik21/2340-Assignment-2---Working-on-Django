
from django import template

register = template.Library()

@register.filter
def get_item(d, key):
    """Safely fetch dict item by key (handles string/int keys)."""
    if not isinstance(d, dict):
        return ""
    return d.get(str(key)) if str(key) in d else d.get(key, "")

@register.filter
def mul(a, b):
    """Multiply two numbers (for subtotal)."""
    try:
        return float(a) * float(b)
    except Exception:
        return ""
