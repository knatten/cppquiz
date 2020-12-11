import datetime
import json
import sys
from pathlib import Path

import tweepy
from django.core.management.base import BaseCommand

from cppquiz.quiz.models import Question

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--skip-tweet', action='store_true')

    def handle(self, *args, **options):
        skip_tweet = options["skip_tweet"]

        for q in Question.objects.filter(state='SCH', publish_time__lte=datetime.datetime.now()):
            print(f"Publishing question {q}")
            q.state = 'PUB'
            q.save()
            if (q.tweet_text):
                print(f"Posting to Twitter: '{q.tweet_text}'")
                if skip_tweet:
                    print("Skipping!")
                else:
                    self.tweet(q.tweet_text)

    def tweet(self, content):
        try:
            secrets_file = Path.home() / ".cppquiz-secrets.json"
            with secrets_file.open() as f:
                secrets = json.load(f)
            auth = tweepy.OAuthHandler(secrets["consumer_key"],secrets["consumer_secret"])
            auth.set_access_token(secrets["key"], secrets["secret"])
            api = tweepy.API(auth)
            api.update_status(content)
        except Exception as e:
            print(f"Failed to tweet '{content}' due to exception '{e}'")
            sys.exit(1)
