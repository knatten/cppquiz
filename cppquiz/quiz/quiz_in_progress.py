from answer import Answer
from models import Quiz

class QuestionStats:
    def __init__(self, skipped=False):
        self.skipped = skipped

#TODO akn what if there are two in progress...
class QuizInProgress:
    def __init__(self, session, quiz):
        self.session = session
        self.quiz = quiz
        if session.has_key('quiz_in_progress'):
            self.answers = session['quiz_in_progress'].answers
            self.previous_result = session['quiz_in_progress'].previous_result
        else:
            self.answers = []
            self.previous_result = None

    def get_current_question(self):
        return self.quiz.questions.all()[len(self.answers)]

    def get_previous_result(self):
        return self.previous_result

    def nof_answered_questions(self):
        return len(self.answers)

    def get_total_nof_questions(self):
        return self.quiz.questions.count()

    def is_finished(self):
        return self.quiz.questions.count() == self.nof_answered_questions()

    def score(self):
        return len([q for q in self.answers if not q.skipped])

    def answer(self, request):
        answer = Answer(self.get_current_question(), request)
        if answer.correct:
            self.answers.append(QuestionStats())
            self.previous_result = 'correct'
        else:
            self.previous_result = 'incorrect'
        return

    def skip(self):
        self.previous_result = None
        self.answers.append(QuestionStats(skipped=True))

    def save(self):
        self.session.modified = True
        self.session['quiz_in_progress'] = self
        self.session.set_expiry(60*60*24*365*10) #TODO akn DRY


def clear_quiz_in_progress(session):
    if session.has_key('quiz_in_progress'):
        session.pop('quiz_in_progress')
