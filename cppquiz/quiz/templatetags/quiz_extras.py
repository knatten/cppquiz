# -*- coding: utf-8 -*-
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


@register.filter(needs_autoescape=True)
def standard_ref(text, autoescape=None):
    if autoescape:
        text = conditional_escape(text)
    return mark_safe(
        re.sub(u'(§[\d\.]+[¶\d]*)', '<em>\\1</em>', text))

@register.filter(needs_autoescape=True)
def emphasize(text, autoescape=None):
    if autoescape:
        text = conditional_escape(text)
    return mark_safe(
        re.sub(u'\*\*\*(.*)\*\*\*', '<em>\\1</em>', text))
