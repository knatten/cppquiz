import json
import sys
import requests
from datetime import datetime, timezone
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
            if (q.socials_text):
                if skip_socials:
                    print("Skipping posting to social media!")
                else:
                    self.post_to_x(q.socials_text)
                    self.post_to_bluesky(q.socials_text)
                    self.post_to_mastodon(q.socials_text)

    def post_to_x(self, content):
        print(f"Posting to X: '{content}'")
        try:
            secrets = self.read_secrets()

            client = tweepy.Client(
                consumer_key=secrets["consumer_key"], consumer_secret=secrets["consumer_secret"],
                access_token=secrets["access_token"], access_token_secret=secrets["access_token_secret"],
            )
            response = client.create_tweet(
                text=content
            )
            post_url = f"https://x.com/user/status/{response.data['id']}"
            print(f"Posted {post_url}")
        except Exception as e:
            print(f"Failed to post '{content}' to X due to exception '{e}'")
            sys.exit(1)

    def post_to_bluesky(self, content):
        print(f"Posting to Bluesky: '{content}'")
        secrets = self.read_secrets()

        resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": "cppquiz.bsky.social", "password": secrets["bsky_password"]},
        )
        resp.raise_for_status()
        session = resp.json()

        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        post = {
            "$type": "app.bsky.feed.post",
            "text": content,
            "createdAt": now,
        }

        resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": "Bearer " + session["accessJwt"]},
            json={
                "repo": session["did"],
                "collection": "app.bsky.feed.post",
                "record": post,
            },
        )
        resp.raise_for_status()

    def post_to_mastodon(self, content):
        print(f"Posting to Mastodon: '{content}'")
        secrets = self.read_secrets()

        url = "https://mastodon.online/api/v1/statuses"
        auth = {"Authorization": f"Bearer {secrets['mastodon_token']}"}
        params = {"status": content}

        r = requests.post(url, data=params, headers=auth)
        r.raise_for_status()


    def read_secrets(self):
        secrets_file = Path.home() / ".cppquiz-secrets.json"
        with secrets_file.open() as f:
            return json.load(f)
