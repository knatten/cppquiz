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
def code_blocks(text, autoescape=None):
    if autoescape:
        text = conditional_escape(text)
    new_text = ''
    lines = text.splitlines(True)
    in_code_block = False
    for line in lines:
        if not in_code_block and line.startswith('    '):
            new_text += '</p><pre class="sh_cpp sh_sourceCode">'
            in_code_block = True
        if in_code_block and not line.startswith('    '):
            new_text += '</pre><p>'
            in_code_block = False
        new_text += line
    if in_code_block:
        new_text += '</pre><p>'
    return mark_safe(new_text)


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
        re.sub(u'\*\*\*(.*)\*\*\*', '<strong>\\1</strong>', text))
