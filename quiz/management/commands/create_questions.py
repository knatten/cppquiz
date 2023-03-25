from random import randint
from django.core.management.base import BaseCommand
from quiz.models import *


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('nof_questions', metavar='N', nargs=1, type=int)

    def handle(self, *args, **options):
        print(options['nof_questions'])
        for i in range(0, options['nof_questions'][0]):
            q = Question.objects.create(question='', answer='', result='OK', state='PUB',
                                        hint='no hint', difficulty=randint(1, 3), explanation='')
            q.question = question.replace("pk", str(q.pk))
            q.answer = str(q.pk)
            q.hint = "It's " + str(q.pk)
            q.comment = "I'm pretty sure it's " + str(q.pk)
            q.explanation = "Because " + str(q.pk) + ", see §[over.best.ics]¶6 in the standard."
            q.save()


question = """#include <iostream>

int main()
{
    std::cout << pk;
} """
