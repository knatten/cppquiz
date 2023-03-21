from django.core.management.base import BaseCommand

from quiz.models import Question, generate_preview_key


class Command(BaseCommand):

    def handle(self, *args, **options):
        questions = Question.objects.filter(preview_key='')
        print(f"Found {len(questions)} questions without a preview key, assigning them one")
        for question in Question.objects.filter(preview_key=''):
            question.preview_key = generate_preview_key()
            question.save()
            print(".", end="")
        print("\nDone")
