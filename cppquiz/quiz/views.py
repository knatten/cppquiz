# Create your views here.

import random

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from quiz.models import Question

def index(request):
    return HttpResponseRedirect(get_url_for_unanswered_question(request.session))

def clear(request):
    request.session.clear()
    return HttpResponseRedirect(get_url_for_unanswered_question(request.session))

def question(request, question_id):
    q = Question.objects.get(id=question_id) #TODO use get or 404
    d = {}
    d['answered'] = False
    d['question'] = q.question .replace('<', '&lt;') .replace('>', '&gt;') .replace('[cpp]', '<pre class="sh_cpp">') .replace('[/cpp]', '</pre>')
    if request.REQUEST.get('did_answer'):
        register_correct_answer(request.session, question_id)
        d['answered'] = True
        if request.REQUEST.get('answer').strip() == q.answer.strip():
            d['correct_result'] = 'yay'
    d['stats'] = get_stats(request.session)
    d['next_question'] = get_url_for_unanswered_question(request.session)
    d['is_staff'] = request.user.is_staff
    return render_to_response('quiz/index.html',
        d,
        context_instance=RequestContext(request)
        )

#TODO what if there are no questions
def get_url_for_unanswered_question(session):
    available_questions = [q.id for q in Question.objects.all()]
    answered_questions = list(session.get('correct', []))
    for q in answered_questions:
        available_questions.remove(int(q))
    if len(available_questions) == 0:
        random_id = Question.objects.order_by('?')[0].id
    else:
        random_id = random.choice(available_questions)
    return '/quiz/question/' + str(random_id)

def get_url_for_random_question():
    random_id = Question.objects.order_by('?')[0].id
    return '/quiz/question/' + str(random_id)

def get_stats(session):
    total = Question.objects.count()
    return {
        'correct': len(session.get('correct', [])),
        'total':total,
        }
def register_correct_answer(session, question_id):
    if not session.has_key('correct'):
        session['correct'] = set()
    session['correct'].add(question_id)
    session.modified=True
