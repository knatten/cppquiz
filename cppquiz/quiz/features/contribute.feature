Feature: Contributing Questions
    Scenario: User contributes a valid question
        When I visit /quiz/create
        Then I should see the contribute form
        Then I fill in "foo" as the question and "bar" as the explanation
        Then The administrators should get an email about a new question

    Scenario: User forgets to enter the question itself
        When I visit /quiz/create
        Then I should see the contribute form
        Then I fill in "" as the question and "bar" as the explanation
        Then There is an error "This field can not be empty." in question

    Scenario: User forgets to enter an explanation
        When I visit /quiz/create
        Then I should see the contribute form
        Then I fill in "foo" as the question and "" as the explanation
        Then There is an error "This field can not be empty." in explanation
