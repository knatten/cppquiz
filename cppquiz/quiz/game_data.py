class UserData:
    def __init__(self, session):
        if session.has_key('user_data'):
            self.correctly_answered = session['user_data'].correctly_answered
        else:
            self.correctly_answered = set()

    def get_correctly_answered_questions(self):
        return list(self.correctly_answered)

    def register_correct_answer(self, question_id):
        self.correctly_answered.add(question_id)

    def clear_correct_answers(self):
        self.correctly_answered.clear()

def save_user_data(user_data, session):
    session.modified = True
    session['user_data'] = user_data
    session.set_expiry(60*60*24*365*10)
