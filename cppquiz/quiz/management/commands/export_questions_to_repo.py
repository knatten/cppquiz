import codecs
import json
import os

from django.core.management.base import BaseCommand
from cppquiz.quiz.models import Question
from cppquiz import settings
from django.db.models import Q

class Command(BaseCommand):


    def add_arguments(self, parser):
        parser.add_argument('repo_root', nargs=1)

    def handle(self, *args, **options):
        repo_root = options['repo_root'][0]
        print("Repo root is '" + repo_root + "'")
        for q in Question.objects.filter(Q(state='PUB') | Q(state='ACC')):
            print("Exporting question " + str(q.id))
            meta_data = {
                "id": q.id,
                "result" : q.result,
                "answer" : q.answer,
                "state" : q.state,
                "difficulty" : q.difficulty,
            }
            question_root = os.path.join(repo_root, str(q.id))
            os.mkdir(question_root)
            with open(os.path.join(question_root, 'meta_data.json'), 'w') as f:
                f.write(json.dumps(meta_data, indent=4))
            with codecs.open(os.path.join(question_root, 'question.cpp'), 'w', 'utf-8') as f:
                f.write(q.question)
            with codecs.open(os.path.join(question_root, 'hint.md'), 'w', 'utf-8') as f:
                f.write(q.hint)
            with codecs.open(os.path.join(question_root, 'explanation.md'), 'w', 'utf-8') as f:
                f.write(q.explanation)
            with codecs.open(os.path.join(question_root, 'README.md'), 'w', 'utf-8') as f:
                result_display = q.get_result_display().replace('is undefined', 'has undefined behavior') 
                if q.result == 'OK':
                    result_display = result_display + ' `' + q.answer + '`'
                readme = readme_template.replace('{{ANSWER}}', result_display)
                f.write(readme)


readme_template = """
### Thanks for helping!

Thank you for helping to port this question from C++11 to C++17.

You'll find the source code in [question.cpp](question.cpp), this should normally not need modification.

In C++11, the correct answer is:
> {{ANSWER}}

Please verify that this is still correct in C++17. If it is, please do the following:
- Update [explanation.md](explanation.md):
  - Refer to the correct section numbers
  - Use updated quotes from those sections (the wording might have changed)
  - Make sure the rest of the text in the explanation is consistent with the new standard
- Update [hint.md](hint.md) if needed (usually not needed)

If the correct answer has changed from C++11 to C++17, you can either just leave a comment in this issue and assign it to @knatten, or see the instructions for [updating meta data](/METADATA_HOWTO.md).
"""
