import json

from collections import defaultdict

from quiz.util import save_data_in_session


class UserData:
    def __init__(self):
        self.correctly_answered: set[int] = set()
        self.dismissed_training_msg: bool = False
        self.attempts: defaultdict[int, int] = defaultdict(int)

    def get_correctly_answered_questions(self):
        return self.correctly_answered

    def register_correct_answer(self, question_id: int):
        self.correctly_answered.add(question_id)

    def clear_correct_answers(self):
        self.correctly_answered.clear()

    def dismiss_training_msg(self):
        self.dismissed_training_msg = True

    def register_attempt(self, question_id: int):
        self.attempts[question_id] += 1

    def attempts_given_for(self, question_id):
        return self.attempts[int(question_id)]

    def to_json(self):
        return json.dumps(
            {'correctly_answered': list(self.correctly_answered), 'dismissed_training_msg': self.dismissed_training_msg,
             'attempts': self.attempts, })

    @staticmethod
    def from_json(user_data_str: str):
        this = UserData()
        user_data = json.loads(user_data_str)
        if 'correctly_answered' in user_data:
            this.correctly_answered.update(user_data['correctly_answered'])
        if 'dismissed_training_msg' in user_data:
            this.dismissed_training_msg = user_data['dismissed_training_msg']
        if 'attempts' in user_data:
            for key, value in user_data['attempts'].items():
                this.attempts[int(key)] = value
        return this


def save_user_data(user_data, session):
    save_data_in_session({'user_data': user_data.to_json()}, session)


def load_user_data(session):
    return UserData.from_json(session['user_data']) if 'user_data' in session else UserData()
