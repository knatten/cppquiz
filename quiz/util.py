from quiz.models import Question


def get_published_questions():
    return Question.objects.filter(state='PUB')


def get_next_published_question(question):
    return Question.objects.filter(state='PUB', pk__gt=question.id).order_by("pk").first()


def get_previous_published_question(question):
    return Question.objects.filter(state='PUB', pk__lt=question.id).order_by("-pk").first()
