from django.core.management.base import BaseCommand, CommandError
from cppquiz.quiz.models import *

class Command(BaseCommand):
#    args = '<poll_id poll_id ...>'
#    help = 'Closes the specified poll for voting'
    max_line_length = 60

    def handle(self, *args, **options):
        print("CHECKING FOR LONG LINES:")
        for question in Question.objects.all():
            for line in question.question.splitlines():
                if len(line) > self.max_line_length:
                    print("In question", question.pk, ":")
                    print(line)
        print()
        print("CHECKING FOR MISSING HINTS")
        for question in Question.objects.all():
            if question.state == 'PUB' and len(question.hint) < 10:
                print("Question", question.pk, "is published and missing a hint")
