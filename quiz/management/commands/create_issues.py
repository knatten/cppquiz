import json
import urllib.error
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand
from django.db.models import Q

from quiz.management.commands import text_generator
from quiz.models import Question


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('user', nargs=1)
        parser.add_argument('repo', nargs=1)
        parser.add_argument('token', nargs=1)

    def handle(self, *args, **options):
        for q in Question.objects.filter(Q(state='PUB') | Q(state='ACC')):
            print("Creating issue for " + str(q.id))
            title = 'Update question ' + str(q.id)
            body = text_generator.get_issue(q)
            data = json.dumps({'issue': {'title': title, 'body': body}}).encode("utf-8")
            url = 'https://api.github.com/repos/' + options['user'][0] + '/' + options['repo'][0] + '/import/issues'
            headers = {
                'Authorization': 'token ' + options['token'][0],
                'Accept': 'application/vnd.github.golden-comet-preview+json'
            }
            request = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(request)
            print(response.read())
