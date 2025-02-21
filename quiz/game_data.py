from collections import defaultdict

from quiz.models import Question
from quiz.util import save_data_in_session


class UserData:
    def __init__(self, correctly_answered: set[int] = None, dismissed_training_msg: bool = False, attempts: dict[int, int] = None):
        self.correctly_answered = correctly_answered if correctly_answered is not None else set()
        self.dismissed_training_msg = dismissed_training_msg
        self.attempts = defaultdict(int, attempts if attempts is not None else {})

    def get_correctly_answered_questions(self):
        return set(Question.objects.filter(pk__in=self.correctly_answered, state='PUB').values_list('pk', flat=True))

    def register_correct_answer(self, question_id):
        self.correctly_answered.add(question_id)

    def clear_correct_answers(self):
        self.correctly_answered.clear()

    def dismiss_training_msg(self):
        self.dismissed_training_msg = True

    def register_attempt(self, answer):
        self.attempts[int(answer.question.pk)] += 1

    def attempts_given_for(self, question_id):
        return self.attempts[int(question_id)]

    def to_dict(self):
        return {'correctly_answered': list(self.correctly_answered),
                'dismissed_training_msg': self.dismissed_training_msg,
                'attempts': list(self.attempts.items())}

    @staticmethod
    def from_dict(data):
        return UserData(set(data['correctly_answered']), data['dismissed_training_msg'], dict(data['attempts']))


def save_user_data(user_data, session):
    save_data_in_session({'user_data': user_data.to_dict()}, session)


def load_user_data(session):
    if 'user_data' in session:
        return UserData.from_dict(session['user_data'])
    return UserData()
