Feature: Fixed quizzes
    Scenario: User is offered to start
        When I am answering random questions
        Then I should be offered to start a quiz

    Scenario: User who mistypes a quiz url gets suggestions
        When I mistype a quiz
        Then I should see suggestions for quizzes with similar keys
