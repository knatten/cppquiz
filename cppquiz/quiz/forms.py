from django.forms import ModelForm
from django.core.exceptions import ValidationError
from models import Question

def cannot_be_empty(field):
    if len(field) == 0:
        raise ValidationError('This field can not be empty.')
    return field

class QuestionForm(ModelForm):

    class Meta:
        model = Question

    def clean_question(self):
        return cannot_be_empty(self.cleaned_data['question'])

    def clean_explanation(self):
        return cannot_be_empty(self.cleaned_data['explanation'])
