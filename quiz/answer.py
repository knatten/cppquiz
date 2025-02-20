from quiz.models import Question, UsersAnswer


class Answer:
    def __init__(self, question: Question, given_answer: str, given_result: str):
        self.question = question
        self.given_answer = given_answer
        self.given_result = given_result
        self.correct = self.given_result == self.question.result and\
            (self.question.result != 'OK' or self.given_answer == self.question.answer.strip())

    def register_given_answer(self):
        UsersAnswer.objects.create(
            question=self.question,
            answer=self.given_answer,
            result=self.given_result,
            correct=self.correct)
