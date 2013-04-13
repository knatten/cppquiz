# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from quiz.models import Question

def index(request):
    return HttpResponseRedirect(get_url_for_random_question())

def question(request, question_id):
    q = Question.objects.get(id=question_id) #TODO what if there are no questions yet
    d = {}
    d['next_question'] = get_url_for_random_question()
    d['answered'] = False
    d['question'] = q.question .replace('<', '&lt;') .replace('>', '&gt;') .replace('[cpp]', '<pre class="sh_cpp">') .replace('[/cpp]', '</pre>')
    if request.REQUEST.get('did_answer'):
        register_correct_answer(request.session, question_id)
        d['answered'] = True
        if request.REQUEST.get('answer').strip() == q.answer.strip():
            d['correct_result'] = 'yay'
    d['stats'] = get_stats(request.session)
    return render_to_response('quiz/index.html',
        d,
        context_instance=RequestContext(request)
        )

def get_url_for_random_question():
    random_id = Question.objects.order_by('?')[0].id
    return '/quiz/question/' + str(random_id)

def get_stats(session):
    total = Question.objects.count()
    print "SESSION", session.get('correct')
    return {
        'correct': len(session.get('correct', [])),
        'total':total,
        }
def register_correct_answer(session, question_id):
    if not session.has_key('correct'):
        session['correct'] = set()
    session['correct'].add(question_id)
    session.modified=True
