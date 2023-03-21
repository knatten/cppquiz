from quiz.models import Question


def get_published_questions():
    return Question.objects.filter(state='PUB')
