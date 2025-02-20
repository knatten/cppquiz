from dataclasses import dataclass, asdict

from quiz.util import save_data_in_session
from quiz.models import Quiz


@dataclass
class QuestionStats:
    skipped: bool = False
    attempts: int = 0
    used_hint: bool = False

    def score(self):
        score = self.skipped == False
        if self.used_hint:
            score -= .5
        score *= pow(.5, self.attempts)
        return score


class QuizInProgress:
    def __init__(self, quiz_key: str, question_stats: list = None, previous_result: str = None, previous_explanation: str = None, attempts: int = 0, used_hint: int = 0):
        self.quiz = Quiz.objects.get(key=quiz_key)
        self.key = self.quiz.key
        self.question_stats = question_stats if question_stats is not None else []
        self.previous_result = previous_result
        self.previous_explanation = previous_explanation
        self.attempts = attempts
        self.used_hint = used_hint

    def get_current_question(self):
        try:
            return self.quiz.get_ordered_questions()[len(self.question_stats)]
        except IndexError:
            raise Exception("%d questions, %d answers" % (self.quiz.questions.count(), len(self.question_stats)))

    def get_previous_result(self):
        return self.previous_result

    def get_previous_explanation(self):
        return self.previous_explanation

    def nof_answered_questions(self):
        return len(self.question_stats)

    def get_total_nof_questions(self):
        return self.quiz.questions.count()

    def is_finished(self):
        return self.quiz.questions.count() == self.nof_answered_questions()

    def score(self):
        return float(sum([q.score() for q in self.question_stats]))

    def answer(self, answer):
        answer.register_given_answer()
        if answer.correct:
            self.question_stats.append(QuestionStats(attempts=self.attempts, used_hint=self.used_hint))
            self._reset_question_state()
            self.previous_result = 'correct'
            self.previous_explanation = answer.question.explanation
        else:
            self.previous_result = 'incorrect'
            self.attempts += 1
        return

    def use_hint(self):
        self.used_hint = 1

    def skip(self):
        if self.is_finished():
            return
        self._reset_question_state()
        self.question_stats.append(QuestionStats(skipped=True))

    def to_dict(self):
        return {
            'quiz_key': self.quiz.key,
            'question_stats': [asdict(qs) for qs in self.question_stats],
            'previous_result': self.previous_result,
            'previous_explanation': self.previous_explanation,
            'attempts': self.attempts,
            'used_hint': self.used_hint,
        }

    @classmethod
    def from_dict(cls, data):
        question_stats = [QuestionStats(**qs) for qs in data['question_stats']]
        return QuizInProgress(
            quiz_key=data['quiz_key'],
            question_stats=question_stats,
            previous_result=data['previous_result'],
            previous_explanation=data['previous_explanation'],
            attempts=data['attempts'],
            used_hint=data['used_hint'],
        )

    def _reset_question_state(self):
        self.previous_explanation = None
        self.previous_result = None
        self.attempts = 0
        self.used_hint = 0


def save_quiz_in_progress(quiz_in_progress, session):
    save_data_in_session({'quiz_in_progress': quiz_in_progress.to_dict()}, session)


def load_quiz_in_progress(session):
    if 'quiz_in_progress' in session:
        return QuizInProgress.from_dict(session['quiz_in_progress'])
    return None


def clear_quiz_in_progress(session):
    if 'quiz_in_progress' in session:
        session.pop('quiz_in_progress')
