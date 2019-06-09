# -*- coding: utf-8 -*-
import re
import markdown

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def format_paragraph(section_name, paragraph_number, full_text, after_char):
    if after_char:
        full_text = full_text[:-1]
    if section_name:
        prefix = "https://timsong-cpp.github.io/cppwp/n4659/"
        full_link = prefix + section_name
        if paragraph_number:
            full_link = full_link + "#" + paragraph_number
        return "<em><a href=\"" + full_link + "\">" + full_text + "</a></em>" + after_char
    else:
        return "<em>" + full_text + "</em>" + after_char

def standard_ref(text):
    possible_named_reference = u'(\[(\w+(\.\w+)*)\])?'
    numbered_reference = u'§\d+(\.\d+)*'
    possible_pilcrow_reference = u'(¶(\d+(\.\d+)*))*'
    regex = re.compile('(' + possible_named_reference + '\(?' + numbered_reference + '\)?' + possible_pilcrow_reference + ')([^\.\d]?)')
    for m in re.finditer(regex, text):        
        full_paragraph = m.group(0)
        section_name = m.group(3)
        paragraph_number = m.group(7)
        after_char = m.group(9)
        text = text.replace(full_paragraph,
            format_paragraph(section_name, paragraph_number, full_paragraph, after_char))        
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
