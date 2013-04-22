# Create your views here.

import random

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import mail_admins

from quiz.models import Question, UsersAnswer
from quiz.forms import QuestionForm

def index(request):
    return HttpResponseRedirect(get_url_for_unanswered_question(request.session))

def clear(request):
    request.session.clear()
    return HttpResponseRedirect(get_url_for_unanswered_question(request.session))

#http://stackoverflow.com/a/4581997
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class Answer():
    def __init__(self, question, request):
        self.question = question
        self.given_answer = request.REQUEST.get('answer').strip()
        self.given_result = request.REQUEST.get('result').strip()
        self.correct = self.given_result == self.question.result and\
            (self.question.result != 'OK' or self.given_answer == self.question.answer.strip())
        self.ip = get_client_ip(request)

    def register_given_answer(self):
        UsersAnswer.objects.create(
            question=self.question,
            answer=self.given_answer,
            result=self.given_result,
            correct=self.correct,
            ip=self.ip)

def create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            mail_admins('Someone made a question!', 'http://' + request.get_host() + '/admin/quiz/question/?published__exact=0')
            return HttpResponseRedirect('/quiz/created')
    else:
        form = QuestionForm()
    return render_to_response('quiz/create.html',
        {'form':form},
        context_instance=RequestContext(request)
        )

def question(request, question_id):
    request.session.set_expiry(60*60*24*365*10)
    q = get_object_or_404(Question, id=question_id, published=True)
    d = {}
    d['answered'] = False
    d['question'] = q
    if request.REQUEST.get('did_answer'):
        d['answered'] = True
        answer = Answer(q, request)
        answer.register_given_answer()
        if answer.correct:
            d['correct_result'] = True
            register_correct_answer(request.session, question_id)
    d['stats'] = get_stats(request.session)
    d['next_question'] = get_url_for_unanswered_question(request.session)
    d['is_staff'] = request.user.is_staff
    return render_to_response('quiz/index.html',
        d,
        context_instance=RequestContext(request)
        )

def is_answer_correct(q, given_answer, given_result):
    return given_result == q.result and (q.result != 'OK' or given_answer == q.answer.strip())

#TODO what if there are no questions
def get_url_for_unanswered_question(session):
    available_questions = [q.id for q in Question.objects.filter(published=True)]
    answered_questions = list(session.get('correct', []))
    for q in answered_questions:
        available_questions.remove(int(q))
    if len(available_questions) == 0:
        random_id = Question.objects.filter(published=True).order_by('?')[0].id
    else:
        random_id = random.choice(available_questions)
    return '/quiz/question/' + str(random_id)

def get_stats(session):
    total = Question.objects.filter(published=True).count()
    return {
        'correct': len(session.get('correct', [])),
        'total':total,
        }
def register_correct_answer(session, question_id):
    if not session.has_key('correct'):
        session['correct'] = set()
    session['correct'].add(question_id)
    session.modified=True
