import codecs
import json
import os

from django.core.management.base import BaseCommand

from quiz.models import Question


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('repo_root', nargs=1)

    def get_question_ids(self, questions_root):
        return [d for d in os.listdir(questions_root) if os.path.isdir(os.path.join(questions_root, d))]

    def handle(self, *args, **options):
        questions_root = os.path.join(options['repo_root'][0], 'questions')
        print("Questions root is '" + questions_root + "'")
        if (not os.path.isdir(questions_root)):
            raise Exception("Questions root '" + questions_root + "'does not exist or is not a directory!")

        question_ids = self.get_question_ids(questions_root)
        self.check_that_questions_exist(question_ids)
        self.update_questions(questions_root, question_ids)

    def check_that_questions_exist(self, question_ids):
        print("Checking that all questions are in the database...")
        for question_id in question_ids:
            Question.objects.get(pk=question_id)
        print("ok")

    def update_questions(self, questions_root, question_ids):
        print("Updating all questions...")
        for question_id in question_ids:
            self.update_question(questions_root, question_id)

    def update_question(self, questions_root, question_id):
        question_root = os.path.join(questions_root, question_id)
        print("Updating question '" + question_id + "' from '" + question_root + "'")
        question = Question.objects.get(pk=question_id)
        self.set_meta_data(question, os.path.join(question_root, 'meta_data.json'))
        self.set_question(question, os.path.join(question_root, 'question.cpp'))
        self.set_hint(question, os.path.join(question_root, 'hint.md'))
        self.set_explanation(question, os.path.join(question_root, 'explanation.md'))
        question.save()

    def set_meta_data(self, question, meta_data):
        with open(meta_data, 'r') as f:
            meta_data = json.loads(f.read())
            question.answer = meta_data['answer']
            question.difficulty = meta_data['difficulty']
            question.state = meta_data['state']
            question.result = meta_data['result']

    def set_question(self, question, source):
        with codecs.open(source, 'r', 'utf-8') as f:
            question.question = f.read()

    def set_hint(self, question, hint):
        with codecs.open(hint, 'r', 'utf-8') as f:
            question.hint = f.read()

    def set_explanation(self, question, explanation):
        with codecs.open(explanation, 'r', 'utf-8') as f:
            question.explanation = f.read()
