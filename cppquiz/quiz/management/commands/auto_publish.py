import datetime
import json
from pathlib import Path

import tweepy
from django.core.management.base import BaseCommand

from cppquiz.quiz.models import Question

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--skip-tweet', action='store_true')

    def handle(self, *args, **options):
        skip_tweet = options["skip_tweet"]
        print(f"Auto publishing questions")

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
        secrets_file = Path.home() / ".cppquiz-secrets.json"
        with secrets_file.open() as f:
            secrets = json.load(f)
        auth = tweepy.OAuthHandler(secrets["consumer_key"],secrets["consumer_secret"])
        auth.set_access_token(secrets["key"], secrets["secret"])
        api = tweepy.API(auth)
        status = api.update_status(content)
        print(status)
