import codecs
import json
import os

from django.core.management.base import BaseCommand
from cppquiz.quiz.models import Question
from cppquiz import settings
from django.db.models import Q
from . import text_generator

class Command(BaseCommand):


    def add_arguments(self, parser):
        parser.add_argument('repo_root', nargs=1)

    def handle(self, *args, **options):
        repo_root = options['repo_root'][0]
        questions_root = os.path.join(repo_root, 'questions')
        print("Repo root is '" + repo_root + "'")
        if not os.path.isdir(repo_root):
            raise Exception("Repo root '" + repo_root + "' does not exist.")
        if not os.path.isdir(questions_root):
            os.mkdir(questions_root)

        print("Writing instructions")
        with open(os.path.join(repo_root, 'METADATA_HOWTO.md'), 'w') as f:
            f.write(text_generator.meta_data_howto)
        with open(os.path.join(repo_root, 'README.md'), 'w') as f:
            f.write(text_generator.main_readme)

        print("Exporting questions")
        for q in Question.objects.filter(Q(state='PUB') | Q(state='ACC')):
            print("Exporting question " + str(q.id))
            meta_data = {
                "id": q.id,
                "result" : q.result,
                "answer" : q.answer,
                "state" : q.state,
                "difficulty" : q.difficulty,
            }
            question_root = os.path.join(questions_root, str(q.id))
            os.mkdir(question_root)
            with open(os.path.join(question_root, 'meta_data.json'), 'w') as f:
                f.write(json.dumps(meta_data, indent=4))
            with codecs.open(os.path.join(question_root, 'question.cpp'), 'w', 'utf-8') as f:
                f.write(q.question)
            with codecs.open(os.path.join(question_root, 'hint.md'), 'w', 'utf-8') as f:
                f.write(q.hint)
            with codecs.open(os.path.join(question_root, 'explanation.md'), 'w', 'utf-8') as f:
                f.write(q.explanation)
            with codecs.open(os.path.join(question_root, 'README.md'), 'w', 'utf-8') as f:
                f.write(text_generator.get_readme(q))

