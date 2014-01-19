from collections import defaultdict

class UserData:
    def __init__(self, session):
        if session.has_key('user_data'):
            self.correctly_answered = getattr(session['user_data'], 'correctly_answered', set())
            self.dismissed_training_msg = getattr(session['user_data'], 'dismissed_training_msg', False)
            self.attempts = getattr(session['user_data'], 'attempts', defaultdict(int))
        else:
            self.correctly_answered = set()
            self.dismissed_training_msg = False
            self.attempts = defaultdict(int)

    def get_correctly_answered_questions(self):
        return list(self.correctly_answered)

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

def save_user_data(user_data, session):
    session.modified = True
    session['user_data'] = user_data
    session.set_expiry(60*60*24*365*10)
