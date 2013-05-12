import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def code_tags(text, autoescape=None):
    if autoescape:
        text = conditional_escape(text)
    return mark_safe(
        re.sub('`(.*?)`', '<code>\\1</code>', text))


