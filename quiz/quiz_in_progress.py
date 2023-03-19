from quiz.answer import Answer


class QuestionStats:
    def __init__(self, skipped=False, attempts=0, used_hint=False):
        self.skipped = skipped
        self.attempts = attempts
        self.used_hint = used_hint

    def score(self):
        score = self.skipped == False
        if self.used_hint:
            score -= .5
        score *= pow(.5, self.attempts)
        return score


class QuizInProgress:
    def __init__(self, session, quiz):
        self.session = session
        self.quiz = quiz
        if 'quiz_in_progress' in session and session['quiz_in_progress'].quiz.key == quiz.key:
            other = session['quiz_in_progress']
            self.answers = other.answers
            self.previous_result = other.previous_result
            self.previous_explanation = getattr(other, 'previous_explanation', '')
            self.attempts = other.attempts
            self.used_hint = other.used_hint
        else:
            self.answers = []
            self._reset_question_state()

    def get_current_question(self):
        try:
            return self.quiz.get_ordered_questions()[len(self.answers)]
        except IndexError:
            raise Exception("%d questions, %d answers" % (self.quiz.questions.count(), len(self.answers)))

    def get_previous_result(self):
        return self.previous_result

    def get_previous_explanation(self):
        return self.previous_explanation

    def nof_answered_questions(self):
        return len(self.answers)

    def get_total_nof_questions(self):
        return self.quiz.questions.count()

    def is_finished(self, request):
        return self.quiz.questions.count() == self.nof_answered_questions()

    def score(self):
        return float(sum([q.score() for q in self.answers]))

    def answer(self, request):
        answer = Answer(self.get_current_question(), request)
        answer.register_given_answer()
        if answer.correct:
            self.answers.append(QuestionStats(attempts=self.attempts, used_hint=self.used_hint))
            self._reset_question_state()
            self.previous_result = 'correct'
            self.previous_explanation = answer.question.explanation
        else:
            self.previous_result = 'incorrect'
            self.attempts += 1
        return

    def use_hint(self):
        self.used_hint = 1

    def skip(self, request):
        if self.is_finished(request):
            return
        self._reset_question_state()
        self.answers.append(QuestionStats(skipped=True))

    def save(self):
        self.session.modified = True
        self.session['quiz_in_progress'] = self
        self.session.set_expiry(60 * 60 * 24 * 365 * 10)  # TODO akn DRY

    def _reset_question_state(self):
        self.previous_explanation = None
        self.previous_result = None
        self.attempts = 0
        self.used_hint = 0


def clear_quiz_in_progress(session):
    if 'quiz_in_progress' in session:
        session.pop('quiz_in_progress')
