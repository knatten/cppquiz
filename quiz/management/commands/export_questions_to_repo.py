import codecs
import json
import os

from django.core.management.base import BaseCommand
from quiz.models import Question
from cppquiz import settings
from django.db.models import Q
from quiz.management.commands import text_generator

class Command(BaseCommand):


    def add_arguments(self, parser):
        parser.add_argument('repo_root', nargs=1)

    def handle(self, *args, **options):
        repo_root = options['repo_root'][0]
        questions_root = os.path.join(repo_root, 'questions')
        dot_github = os.path.join(repo_root, '.github')
        print("Repo root is '" + repo_root + "'")
        if not os.path.isdir(repo_root):
            raise Exception("Repo root '" + repo_root + "' does not exist.")

        write_general_files(repo_root, dot_github)
        write_questions(repo_root, questions_root)

        print('cd ' + repo_root + '&& git init && git add --all && git commit -m"Initial export" && git remote add origin URL && git push -u origin master')


def write_general_files(repo_root, dot_github):
    print("Writing general files")
    if not os.path.isdir(dot_github):
        os.mkdir(dot_github)
    with open(os.path.join(repo_root, 'METADATA_HOWTO.md'), 'w') as f:
        f.write(text_generator.meta_data_howto)
    with open(os.path.join(repo_root, 'README.md'), 'w') as f:
        f.write(text_generator.main_readme)
    with open(os.path.join(dot_github, 'pull_request_template.md'), 'w') as f:
        f.write(text_generator.pull_request_template)

def write_questions(repo_root, questions_root):
    print("Exporting questions")
    if not os.path.isdir(questions_root):
        os.mkdir(questions_root)
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
