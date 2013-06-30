class ActiveQuiz:
    def __init__(self, quiz):
        self.quiz = quiz

    def total_questions(self):
        return self.quiz.questions.count()
