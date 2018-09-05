def get_readme(question):
    return get_template_with_answer(question)\
        .replace('{{BULLET}}', '-')\
        .replace('{{QUESTION_PATH}}', '')\
        .replace('{{ROOT_PATH}}', '/')

def get_issue(question):
    question_path = '../blob/master/questions/' + str(question.id) + '/'
    return get_template_with_answer(question)\
        .replace('{{BULLET}}', '- [ ]')\
        .replace('{{QUESTION_PATH}}', question_path)\
        .replace('{{ROOT_PATH}}', '../blob/master/')\
        .replace('this question', '[this question](' + question_path + ')')

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

If you get stuck, please describe the problem in detail in a comment to the issue, and a maintainer will add the `help wanted` tag so others can chime in.

If the correct answer has changed from C++11 to C++17, you can either just leave a comment in this issue, or see the instructions for [updating meta data]({{ROOT_PATH}}METADATA_HOWTO.md).
"""

meta_data_howto = """
### Updating meta data

If the correct answer for a question has changed, you need to update the `meta_data.json` file in the directory for that question. Here's an example:

```
{
    "answer": "1",
    "difficulty": 2,
    "state": "PUB",
    "id": 1,
    "result": "OK"
}
```

The fields you need to care about are `answer` and `result`:

- `answer`: If the program is supposed to compile and output something, put that output here. If not, set it to `""`.
- `result`: Here you need to set the correct shorthand for an enum. The possible values are:
    - `OK`: The program is guaranteed a certain output
    - `CE`: The program has a compilation error
    - `US`: The program is unspecified / implementation defined
    - `UD`: The program has undefined behavior
"""

main_readme = """
## Porting CppQuiz.org questions to C++17

CppQuiz.org is an open source C++ quiz site. If you're unfamiliar with it, you can read more in [its "About" section](http://cppquiz.org/quiz/about/).

All the CppQuiz questions are currently targetting C++11. We need to update them for C++17. Most questions will still have the same answers, we just need to update the explanations and references to the standard. A few questions will also have different answers.

Doing this all by myself is going to take months, so I would very much appreciate some help from the community. To make this as simple as possible, I've created this repository. There is a [directory for each question](/questions), named after the question number. That directory contains the source code of the question in a `.cpp` file, the hint and explanation in `.md` files, as well as a `README.md` explaining everything you need to do to port the question. There's also an issue for each question, making it easier to track progress. The issue has the same information as the `README.md` file.

### How to help porting questions
There are two ways to contribute, listed below. I prefer the first alternative, but if that prevents you from contributing, the second is also ok.

#### Contributing using a fork and pull requests
1. Fork this repo by clicking the "Fork" button at the top right.
1. Pick the issue for a question you want to port. Add a comment that you'll be handling that issue.
1. Follow the instructions in the issue to port the question.
1. Make a pull request. Porting several questions in one PR is fine.

#### Contributing without a fork
If you think forking and PRs is too cumbersome, or you are not able to do this for other reasons, I'd still appreciate your help:
1. Pick the issue for a question you want to port. Add a comment that you'll be handling that issue.
1. Follow the instructions in the issue to port the question.
1. Paste the updated files as comments to the issue.

### Other ways to help
- Look for questions labeled `help wanted`. It means the person responsible needs a second pair of eyes.
- Look at pull requests, review them and comment `LGTM` if they should be merged.
- Other ideas for help are also welcome, please get in touch (see [Questions](#questions) below).

### Questions
If you have any questions, either file an issue in this repo, contact [@knatten on Twitter](https://twitter.com/knatten), or email me at anders@knatten.org.
"""

pull_request_template = """ Fixes #<issue number> (Make sure to enter the issue number, not the question number! If this PR fixes multiple issues, just duplicate this line.)
"""
