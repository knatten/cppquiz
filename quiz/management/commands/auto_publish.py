import json
import sys
import traceback
import requests
import datetime
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils import timezone

from quiz.models import Question


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--skip-socials', action='store_true')

    def handle(self, *args, **options):
        skip_socials = options["skip_socials"]
        had_failure = False

        for q in Question.objects.filter(state='SCH', publish_time__lte=timezone.now()):
            print(f"Publishing question {q}")
            q.state = 'PUB'
            q.save()
            if q.socials_text:
                if skip_socials:
                    print("Skipping posting to social media!")
                else:
                    had_failure |= self.post_to_socials(q.socials_text)

        if had_failure:
            sys.exit(1)

    def post_to_socials(self, content):
        platforms = [
            ("Bluesky", lambda: self.post_to_bluesky(content)),
            ("Mastodon", lambda: self.post_to_mastodon(content)),
        ]
        had_failure = False
        for name, post in platforms:
            try:
                post()
            except Exception:
                had_failure = True
                print(f"Failed to post question to {name}:", file=sys.stderr)
                traceback.print_exc()
        return had_failure

    def post_to_bluesky(self, content):
        print(f"Posting to Bluesky: '{content}'")
        secrets = self.read_secrets()

        resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": "cppquiz.bsky.social", "password": secrets["bsky_password"]},
        )
        resp.raise_for_status()
        session = resp.json()

        now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

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
