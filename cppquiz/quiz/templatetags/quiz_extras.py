# -*- coding: utf-8 -*-
import base64
import json
import markdown
import re
import urllib.parse

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

def format_reference(match):
    full_reference = match.group(0)
    section_name = match.group('section_name')
    paragraph_number = match.group('paragraph')
    if section_name:
        full_link = "https://timsong-cpp.github.io/cppwp/n4659/" + section_name
        if paragraph_number:
            full_link = full_link + "#" + paragraph_number
        return "<em><a href=\"" + full_link + "\">" + full_reference + "</a></em>"
    else:
        return "<em>" + full_reference + "</em>"

def standard_ref(text):
    possible_section_name = u'(\[(?P<section_name>\w+(\.\w+)*)\])?'
    section_number = u'§\d+(\.\d+)*'
    possible_paragraph = u'(¶(?P<paragraph>\d+(\.\d+)*))*'
    regex = re.compile('(' + possible_section_name + section_number + possible_paragraph + ')')
    return re.sub(regex, format_reference, text)

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

@register.filter()
def cpp_insights_link(question):
    std = settings.CPP_STD.replace("C++","cpp")
    return('https://cppinsights.io/lnk?code=%s&insightsOptions=%s&rev=1.0' %(base64.b64encode(question.question.encode()).decode('utf-8'), std))

@register.filter()
def compiler_explorer_link(question):
    editor = {
        "type": "component",
        "componentName": "codeEditor",
        "componentState": {
            "id": 1,
            "source": question.question,
            "options": {"compileOnChange": True, "colouriseAsm": True},
        },
    }

    compiler = {
        "type": "component",
        "componentName": "compiler",
        "componentState": {
            "source": 1,
            "compiler": "g92",
            "options": f"-std={settings.CPP_STD.lower()}",
        },
    }

    content = [editor, compiler]
    obj = {"version": 4, "content": [{"type": "row", "content": content}]}

    payload = json.dumps(obj)
    ceFragment = urllib.parse.quote(payload)
    url = "https://godbolt.org/#" + ceFragment
    return url
