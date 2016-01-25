import sys
from django.core.management.base import BaseCommand, CommandError
from cppquiz.quiz.models import *

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('nof_questions', metavar='N', nargs=1, type=int)

    def handle(self, *args, **options):
        print options['nof_questions']
        for i in range(0, options['nof_questions'][0]):
            print "Creating a question"
            q = Question.objects.create(question='', answer='', result='OK', published=True, hint='no hint', difficulty=1, explanation='')
            q.question = question.replace("pk", str(q.pk))
            q.answer = str(q.pk)
            q.hint = "It's " + str(q.pk)
            q.explanation = "Because " + str(q.pk)
            q.save()

question = """#include <iostream>

int main()
{
    std::cout << pk;
} """
