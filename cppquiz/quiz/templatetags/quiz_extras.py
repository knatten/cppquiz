# -*- coding: utf-8 -*-
import re
import markdown

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def format_paragraph(section_name, paragraph_number, full_text):
    if section_name:
        prefix = "https://timsong-cpp.github.io/cppwp/n4659/"
        full_link = prefix + section_name
        if paragraph_number:
            full_link = full_link + "#" + paragraph_number
        return "<em><a href=\"" + full_link + "\">" + full_text + "</a></em>"
    else:
        return "<em>" + full_text + "</em>"

def standard_ref(text):
    possible_named_reference = u'(\[(\S+(\.\S+)*)\])?'
    numbered_reference = u'§\d+(\.\d+)*'
    possible_pilcrow_reference = u'(¶(\d+(\.\d+)*))*'
    regex = re.compile('(' + possible_named_reference + '\(?' + numbered_reference + '\)?' + possible_pilcrow_reference + ')')
    matched = regex.findall(text)
    for elem in matched:
        full_paragraph = elem[0]
        section_name = elem[2]
        paragraph_number = elem[6]
        text = text.replace(full_paragraph,
           format_paragraph(section_name, paragraph_number, full_paragraph))
    return text

def custom_linebreaks(text):
    return (text
        .replace("\n", "<br />")
        .replace("</p><br />", "</p>")
        .replace("<br /><p>", "<p>")
        .replace("</pre><br />", "</pre>"))

@register.filter(needs_autoescape=True)
def to_html(text, autoescape=None):
    return mark_safe(
        standard_ref(
            custom_linebreaks(
                markdown.markdown(text))))
