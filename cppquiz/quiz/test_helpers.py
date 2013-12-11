import re

from models import Question

def create_questions(nof_questions):
    for i in range(0, nof_questions):
        Question.objects.create(question=str(i), answer=str(i), result='OK', published=True, hint='hint', difficulty=1, explanation='because ' + str(i))

def get_question_pk(html):
    return int(re.findall('Question #(\d*)', html)[0])
