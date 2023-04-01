# Contributing
Thank you for your interest in contributing to CppQuiz.org!

First, no matter how you want to contribute, be nice and respectful towards others. We have
a [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) that you can read if you're in doubt.

Here are some ways you can help:

## Creating questions

You can [create new questions](https://cppquiz.org/quiz/create) for the site. Please remember to first read the section
at the top of that page and, if you can, add references to the standard that back your explanation.

## Contributing to the implementation

The site itself is implemented in Python/Django and is available as an open source project. We welcome contributions
both in the form of issues and pull requests.

### Filing an issue

Issues can be filed as [GitHub issues](https://github.com/knatten/cppquiz/issues). Please first look for existing
issues, as one might already exist.

If the issue you're filing is about a question on the site having the wrong answer, be aware that the questions on the
site are about what the *C++ standard* says the output should be, not what your particular compiler happens to print.
For some questions, even popular compilers like gcc/clang/msvc have bugs and do not conform to the standard. Some
questions also have undefined behaviour.

### Commenting on issues and pull requests

Often there are open [issues](https://github.com/knatten/cppquiz/issues)
and/or [pull requests](https://github.com/knatten/cppquiz/pulls). Maybe you know something that the people involved
don't, in which case we're grateful for your input.

### Making a pull request

In general, we're happy to accept pull requests. However, please consider the following:

- If you're changing the behaviour of the site, we first have to agree that the new behaviour is actually something we
  want. To save you a lot of work, it's recommended to first propose the changes in
  an [issue](https://github.com/knatten/cppquiz/issues), then after discussing and concluding on what the behaviour
  should be, you can implement it and make a [pull request](https://github.com/knatten/cppquiz/pulls).
- When looking for something to get started on, please prioritise looking at
  existing [issues](https://github.com/knatten/cppquiz/issues), in particular ones tagged with "help wanted". There is
  also a "good first issue" tag for issues that should be easy to get started with.
- Arbitrary refactoring PRs are unlikely to be reviewed/accepted unless they solve a real-life issue. If you want to
  make such a PR, please argue clearly in the PR description for why it is important. If the refactoring is more than a
  few lines, you could also create an issue to discuss it first (see the first bullet point).