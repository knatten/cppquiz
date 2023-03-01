import difflib
import json
import re

from django.core.management.base import BaseCommand, CommandError
from quiz.models import *


def _assert_no_bare_section_numbers(text):
    match = re.search("(?<!(\]))§\d", text)
    if match:
        raise ValueError(f"Text contains a bare section number '{match.group(0)}'!")


def remove_section_numbers(text):
    _assert_no_bare_section_numbers(text)
    return re.sub(r"(\[[\w\.]+\])§\d+(\.\d+)*", "§\g<1>", text)


class Command(BaseCommand):
    version = 1

    def handle(self, *args, **options):
        for q in Question.objects.all():
            print("----------------------------------------------------")
            print(f"**** Removing section numbers for question {q.id}\n")
            for field in ["explanation", "hint"]:
                old = getattr(q, field)
                new = remove_section_numbers(old)
                if old == new:
                    print(f"**** No diff in {field}")
                    continue
                differ = difflib.Differ()
                diff = differ.compare(old.splitlines(keepends=True), new.splitlines(keepends=True))
                print(f"**** Diff in {field}:")
                print("\n".join(diff))
                answer = input("**** Accept diff? [y/n/q]").strip().lower()
                if answer == "y":
                    print("**** Committing diff")
                    setattr(q, field, new)
                    q.save()
                elif answer == "q":
                    print("**** Aborting")
                    return
                else:
                    print("**** Not committing diff!")
