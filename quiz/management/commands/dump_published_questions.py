import json

from django.core.management.base import BaseCommand, CommandError
from quiz.models import *
from cppquiz import settings

class Command(BaseCommand):
    version = 1

    def handle(self, *args, **options):
        questions = []
        for q in Question.objects.filter(state='PUB'):
            questions.append({
                "id": q.id,
                "question": q.question,
                "result": q.result,
                "answer": q.answer,
                "explanation": q.explanation,
                "hint": q.hint,
                "difficulty": q.difficulty,
            })
        print(json.dumps({'version': Command.version, 'cpp_standard': settings.CPP_STD, 'questions': questions}))
