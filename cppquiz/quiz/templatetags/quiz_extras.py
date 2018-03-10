# -*- coding: utf-8 -*-
import re
import markdown

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def standard_ref(text):
    return re.sub(u'(§[\d\.]+[¶\d]*)', '<em>\\1</em>', text)

def custom_linebreaks(text):
    return (text
        .replace("\n", "<br />")
        .replace("</p><br />", "</p>")
        .replace("</pre><br />", "</pre>"))

@register.filter(needs_autoescape=True)
def to_html(text, autoescape=None):
    return mark_safe(
        standard_ref(
            custom_linebreaks(
                markdown.markdown(text))))
