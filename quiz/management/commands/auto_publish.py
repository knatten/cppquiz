import json
import sys
from pathlib import Path

import tweepy
from django.core.mail import mail_admins
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
            socials_message = "No posts to social media"
            if (q.socials_text):
                if skip_socials:
                    print("Skipping posting to social media!")
                else:
                    socials_message = self.post_to_x(q.socials_text)
            mail_admins(f"Published question {q}", socials_message)

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
            post_url = f"https://x.com/user/status/{response.data['id']}"
            print(f"Posted {post_url}")
            return post_url
        except Exception as e:
            print(f"Failed to post '{content}' to X due to exception '{e}'")
            sys.exit(1)
