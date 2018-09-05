def get_readme(question):
    return get_template_with_answer(question)\
        .replace('{{BULLET}}', '-')\
        .replace('{{QUESTION_PATH}}', '')\
        .replace('{{ROOT_PATH}}', '/')

def get_issue(question):
    return get_template_with_answer(question)\
        .replace('{{BULLET}}', '- [ ]')\
        .replace('{{QUESTION_PATH}}', '../blob/master/' + str(question.id) + '/')\
        .replace('{{ROOT_PATH}}', '../blob/master/')

def get_template_with_answer(question):
    return template.replace('{{ANSWER}}', get_result_display(question))

def get_result_display(question):
    result_display = question.get_result_display().replace('is undefined', 'has undefined behavior')
    if question.result == 'OK':
        return result_display + ' `' + question.answer + '`'
    return result_display


template = """
### Thanks for helping!

Thank you for helping to port this question from C++11 to C++17.

You'll find the source code in [question.cpp]({{QUESTION_PATH}}question.cpp), this should normally not need modification.

In C++11, the correct answer is:
> {{ANSWER}}

Please verify that this is still correct in C++17. If it is, please do the following:
{{BULLET}} Update [explanation.md]({{QUESTION_PATH}}explanation.md):
  {{BULLET}} Refer to the correct section numbers
  {{BULLET}} Use updated quotes from those sections (the wording might have changed)
  {{BULLET}} Make sure the rest of the text in the explanation is consistent with the new standard
{{BULLET}} Update [hint.md]({{QUESTION_PATH}}hint.md) if needed (usually not needed)

*Note that some older questions are missing references to the standard, we don't need to fix that now.*

If the correct answer has changed from C++11 to C++17, you can either just leave a comment in this issue and assign it to @knatten, or see the instructions for [updating meta data]({{ROOT_PATH}}METADATA_HOWTO.md).
"""
