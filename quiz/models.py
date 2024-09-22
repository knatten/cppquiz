import random
import re
import string

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def generate_preview_key():
    return ''.join(random.sample(string.ascii_lowercase + string.digits, 10))


class Question(models.Model):
    RESULT_CHOICES = (
        ('OK', 'The program is guaranteed to output:'),
        ('CE', 'The program has a compilation error'),
        ('UD', 'The program is (or may be) undefined'),
        ('US', 'The program is unspecified / implementation defined'),
    )
    DIFFICULTY_CHOICES = (
        (0, 'Not set'),
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Expert'),
    )
    STATE_CHOICES = (
        ('NEW', 'New'),
        ('WAI', 'Waiting'),
        ('ACC', 'Accepted'),
        ('SCH', 'Scheduled'),
        ('REF', 'Refused'),
        ('PUB', 'Published'),
        ('RET', 'Retracted'),
    )
    question = models.TextField(default='', blank=True)
    result = models.CharField(max_length=2, default='OK', choices=RESULT_CHOICES)
    answer = models.CharField(max_length=200, default='', blank=True)
    explanation = models.TextField(default='', blank=True,
                                   help_text='Use markdown, and refer to the standard like this: "§[section.subsection]¶x.y".')
    hint = models.TextField(default='No hint', blank=True,
                            help_text='Use markdown, and refer to the standard like this: "§[section.subsection]¶x.y".')
    comment = models.TextField(default='', blank=True,
                               help_text='Comments for admins and contributors, not displayed on the site')
    date_time = models.DateTimeField(auto_now_add=True, help_text='Time of creation')
    publish_time = models.DateTimeField(null=True, blank=True,
                                        help_text='Time of publishing (will be published then if state is "Scheduled")')
    state = models.CharField(max_length=3, default='NEW', choices=STATE_CHOICES)
    author_email = models.EmailField(max_length=254, blank=True, default='')
    difficulty = models.IntegerField(default=0, choices=DIFFICULTY_CHOICES)
    preview_key = models.CharField(blank=True, max_length=10, default=generate_preview_key)
    last_viewed = models.DateTimeField(null=True, blank=True)
    retraction_message = models.TextField(default='', blank=True, help_text='Use markdown')
    reserved = models.BooleanField(default=False,
                                   help_text='This question is reserved for an event, do not publish yet')
    reservation_message = models.CharField(blank=True, max_length=100,
                                           help_text='Which event the question is reserved for')
    socials_text = models.CharField(blank=True, max_length=280,
                                    help_text='What to post when question gets posted on social media')

    def __str__(self):
        return str(self.pk)

    def clean(self):
        verbs = {'SCH': 'schedule', 'PUB': 'publish', 'ACC': 'accept'}
        if self.state in ('PUB', 'SCH', 'ACC') and self.hint == '':
            raise ValidationError(f'Cannot {verbs[self.state]} a question without a hint')
        if self.state in ('PUB', 'SCH', 'ACC') and self.difficulty == 0:
            raise ValidationError(f'Cannot {verbs[self.state]} a question without a difficulty setting')
        if self.state in ('PUB', 'SCH') and self.reserved:
            raise ValidationError(f'Cannot {verbs[self.state]} a reserved question')
        if self.socials_text and not re.search("https?://", self.socials_text):
            raise ValidationError('Tweets must contain a url!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Question, self).save(*args, **kwargs)

    def mark_viewed(self):
        self.last_viewed = timezone.now()
        self.save()


class UsersAnswer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    result = models.CharField(max_length=2, default='OK', choices=Question.RESULT_CHOICES)
    answer = models.CharField(max_length=200, default='', blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)


class Quiz(models.Model):
    questions = models.ManyToManyField(Question, through='QuestionInQuiz')
    key = models.CharField(max_length=10, default='')
    date_time = models.DateTimeField(auto_now_add=True)

    def get_ordered_questions(self):
        # Order pseudo-randomly but not in order of primary key
        return self.questions.all().order_by('hint', 'id')

    def question_ids(self):
        return ','.join([str(q) for q in self.questions.all()])


class QuestionInQuiz(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
