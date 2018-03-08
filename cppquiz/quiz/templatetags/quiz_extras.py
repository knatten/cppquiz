# -*- coding: utf-8 -*-
import re
import markdown

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.template import defaultfilters

register = template.Library()

def standard_ref(text):
    return re.sub(u'(§[\d\.]+[¶\d]*)', '<em>\\1</em>', text)

def custom_linebreaks(text):
    return text.replace("\n", "<br />")

@register.filter(needs_autoescape=True)
def to_html(text, autoescape=None):
    return mark_safe(
        standard_ref(
            markdown.markdown(
                custom_linebreaks(
                    defaultfilters.urlize(text, False)))))
