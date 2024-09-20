import base64
import json
import re
import urllib.parse

import markdown
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


def format_reference(match):
    full_reference = match.group(0)
    section_name = match.group('section_name')
    paragraph_number = match.group('paragraph')
    full_link = "https://timsong-cpp.github.io/cppwp/std23/" + section_name
    if paragraph_number:
        full_link = full_link + "#" + paragraph_number
    return f"*[{full_reference}]({full_link})*"


def standard_ref(text):
    # https://regex101.com/r/hf2P3X/4
    regex = re.compile(
        r'''
        §\[                       # mandatory section part starts with §[
            (?P<section_name>     #
                [^]]+             # at least one character other than ]
            )                     #
        \]                        # section part must end with ]
        (?:¶                      # optional paragraph part starts with ¶
            (?P<paragraph>        #
                [^\s*]*           # any number of non-whitespace characters except * (to support italicized links)
                [\w&\]<>/^|+%=~-] # we support only those paragraphs that end with the following characters:
                                  # any Unicode letter/digit plus _ (use * instead of _ in Markdown) plus
                                  # characters that shouldn't clash with surrounding punctuation/Markdown
            )                     #
        )?                        #
        ''',
        re.VERBOSE,
    )
    return regex.sub(format_reference, text)


@register.filter(needs_autoescape=True)
def to_html(text, autoescape=None):
    return mark_safe(
        markdown.markdown(
            standard_ref(text), extensions=['nl2br', 'pymdownx.superfences']
        )
    )


@register.filter()
def cpp_insights_link(question):
    std = settings.CPP_STD.replace("C++", "cpp")
    return ('https://cppinsights.io/lnk?code=%s&insightsOptions=%s&rev=1.0' % (base64.b64encode(question.question.encode()).decode('utf-8'), std))


@register.filter()
def compiler_explorer_link(question):
    editor = {
        "type": "component",
        "componentName": "codeEditor",
        "componentState": {
            "id": 1,
            "lang": "c++",
            "source": question.question,
            "options": {"compileOnChange": True, "colouriseAsm": True},
        },
    }

    compiler_details = {
        "gcc": {
            "compiler": "gsnapshot",
            "options": f"-std={settings.CPP_STD.lower()} -Wall -Wextra -Wno-unused -Wunused-value"
        },
        "clang": {
            "compiler": "clang_trunk",
            "options": f"-std={settings.CPP_STD.lower()} -stdlib=libc++ -Wall -Wextra -Wno-unused"
                       " -Wno-unused-parameter -Wunused-result -Wunused-value"
        },
        "msvc": {
            "compiler": "vcpp_v19_latest_x64",
            "options": f"/std:c++latest /W4 /wd4100 /wd4101 /wd4189"
        },
    }

    compiler = {
        "type": "component",
        "componentName": "compiler",
        "componentState": {
            "id": 1,
            "source": 1,
            "filters": {"b": 1, "execute": 1, "intel": 1, "commentOnly": 1, "directives": 1},
            **compiler_details["gcc"],
        },
    }

    output = {
        "type": "component",
        "componentName": "output",
        "componentState": {"compiler": 1, "source": 1},
    }

    executors = [{
        "type": "component",
        "componentName": "executor",
        "componentState": {
            "id": compiler_id,
            "source": 1,
            "compilationPanelShown": 1,
            **compiler_details[compiler_name],
        },
    } for compiler_id, compiler_name in enumerate(("clang", "msvc"), start=1)]

    obj = {
        "version": 4,
        "content": [
            {
                "type": "row",
                "content": [editor,
                            {"type": "column", "content": [compiler, output]},
                            {"type": "column", "width": 25, "content": executors}],
            }
        ],
    }

    payload = json.dumps(obj)
    ceFragment = urllib.parse.quote(payload)
    url = "https://godbolt.org/#" + ceFragment
    return url
