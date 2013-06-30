import random
import string

from models import Question, Quiz, QuestionInQuiz

nof_questions_in_quiz = 10

def get_unique_quiz_key(length):
    key = make_quiz_key(length)
    while Quiz.objects.filter(key=key).count():
        key = make_quiz_key(length)
    return key

def make_quiz_key(length):
    return ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, length))

def create_quiz(nof_questions):
    quiz = Quiz.objects.create()
    question_ids = [q.pk for q in Question.objects.filter(published=True)]
    used_questions = random.sample(question_ids, nof_questions)
    for pk in used_questions:
        qinq = QuestionInQuiz(question=Question.objects.get(pk=pk), quiz=quiz)
        qinq.save()
    quiz.key = get_unique_quiz_key(5)
    quiz.save()
    return quiz.key
