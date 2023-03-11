import re
import string
import random

from quiz.models import Question


def create_questions(nof_questions, **kwargs):
    question_kwargs = kwargs.copy()
    question_kwargs.setdefault('state', 'PUB')
    question_kwargs.setdefault('difficulty', 1)

    questions = []

    for i in range(nof_questions):
        question_kwargs['question'] = kwargs.get('question', str(i))
        question_kwargs['answer'] = kwargs.get('answer', str(i))
        question_kwargs['hint'] = kwargs.get('hint', random_hint())
        question_kwargs['explanation'] = kwargs.get('explanation', f'because {i}')

        questions.append(Question.objects.create(**question_kwargs))

    return questions


def get_question_pk(html):
    return int(re.findall("Question #(\d*)", html)[0])


def random_hint():
    return ''.join(random.sample(string.ascii_letters, 5))
