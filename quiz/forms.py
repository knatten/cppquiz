from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from quiz.models import Question


def cannot_be_empty(field):
    if len(field) == 0:
        raise ValidationError('This field can not be empty.')
    return field


class QuestionForm(ModelForm):

    spam_protection = forms.CharField()

    class Meta:
        model = Question
        fields = ('question', 'result', 'answer', 'explanation', 'hint',
                  'comment', 'difficulty', 'author_email', 'spam_protection')
        widgets = {
            'question': forms.Textarea(attrs={'rows': 20}),
            'hint': forms.Textarea(attrs={'rows': 5}),
            'comment': forms.Textarea(attrs={'rows': 5})
        }

    def clean_question(self):
        return cannot_be_empty(self.cleaned_data['question'])

    def clean_explanation(self):
        return cannot_be_empty(self.cleaned_data['explanation'])

    def clean_spam_protection(self):
        field = self.cleaned_data['spam_protection']
        if field.strip('"') != 'human':
            raise ValidationError("You failed the spam protection! Please type \"human\" into the field below:")
        return field
