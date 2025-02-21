import datetime

from django.core.management.base import BaseCommand
from django.urls import reverse


from quiz.util import get_published_questions
from cppquiz import settings

rss_header = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
    <channel>
        <title>CppQuiz - New Questions</title>
        <link>https://cppquiz.org</link>
        <description>Latest C++ quiz questions from CppQuiz.org</description>
        <language>en-us</language>
        <lastBuildDate>{{last_build_date}}</lastBuildDate>
"""

rss_question = """
        <item>
            <title>Question {{id}}</title>
            <link>{{url}}</link>
            <description>Question {{id}} on CppQuiz.org</description>
            <pubDate>{{pubdate}}</pubDate>
            <guid>{{url}}</guid>
        </item>
"""

rss_footer = """
    </channel>
</rss>
"""


atom_header = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
    <title>CppQuiz - New Questions</title>
    <link href="https://cppquiz.org/" />
    <updated>{{last_build_date}}</updated>
    <author>
        <name>CppQuiz</name>
    </author>
    <id>https://cppquiz.org/</id>
"""

atom_question = """
    <entry>
        <title>Question {{id}}</title>
        <link href="{{url}}" />
        <id>{{url}}</id>
        <updated>{{pubdate}}</updated>
        <summary>Question {{id}} on CppQuiz.org</summary>
    </entry>
"""

atom_footer = """
</feed>
"""


class Command(BaseCommand):
    help = "Generate an RSS or Atom feed for published questions."
    post_count = 20

    def add_arguments(self, parser):
        parser.add_argument(
            "format", choices=["rss", "atom"],
            help="Choose feed format: 'rss' or 'atom'"
        )

    def handle(self, *args, **options):
        feed_format = options["format"]
        header = atom_header if feed_format == "atom" else rss_header
        question = atom_question if feed_format == "atom" else rss_question
        footer = atom_footer if feed_format == "atom" else rss_footer
        time_format = "%Y-%m-%dT%H:%M:%SZ" if feed_format == "atom" else "%a, %d %b %Y %H:%M:%S GMT"

        last_build_date = datetime.datetime.now().strftime(time_format)
        print(header.replace("{{last_build_date}}", last_build_date))

        for q in get_published_questions().order_by('-publish_time')[:self.post_count]:
            url = settings.SITE_URL + reverse('quiz:question', args=[q.pk])
            print(question.replace("{{id}}", str(q.id)).replace("{{url}}", url).replace(
                "{{pubdate}}", q.publish_time.strftime(time_format)))

        print(footer)
