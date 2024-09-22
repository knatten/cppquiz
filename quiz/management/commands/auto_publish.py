import json
import sys
from pathlib import Path

import tweepy
from django.core.management.base import BaseCommand
from django.utils import timezone

from quiz.models import Question


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--skip-socials', action='store_true')

    def handle(self, *args, **options):
        skip_socials = options["skip_socials"]

        for q in Question.objects.filter(state='SCH', publish_time__lte=timezone.now()):
            print(f"Publishing question {q}")
            q.state = 'PUB'
            q.save()
            if (q.tweet_text):
                if skip_socials:
                    print("Skipping posting to social media!")
                else:
                    self.post_to_x(q.tweet_text)

    def post_to_x(self, content):
        print(f"Posting to X: '{content}'")
        try:
            secrets_file = Path.home() / ".cppquiz-secrets.json"
            with secrets_file.open() as f:
                secrets = json.load(f)

            client = tweepy.Client(
                consumer_key=secrets["consumer_key"], consumer_secret=secrets["consumer_secret"],
                access_token=secrets["access_token"], access_token_secret=secrets["access_token_secret"],
            )
            response = client.create_tweet(
                text=content
            )
            print(f"Posted https://x.com/user/status/{response.data['id']}")
        except Exception as e:
            print(f"Failed to post '{content}' to X due to exception '{e}'")
            sys.exit(1)
