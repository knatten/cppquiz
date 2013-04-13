# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from quiz.models import Question

def get_url_for_random_question():
    random_id = Question.objects.order_by('?')[0].id
    return '/quiz/question/' + str(random_id)

def index(request):
    return HttpResponseRedirect(get_url_for_random_question())

def question(request, question_id):
    #TODO what if there are no questions yet
    q = Question.objects.get(id=question_id)
    d = {}
    d['next_question'] = get_url_for_random_question()
    if request.REQUEST.get('did_answer'):
        if request.REQUEST.get('answer').strip() == q.answer.strip():
            d['correct_result'] = 'yay'
            d['result'] = 'yay'
        else:
            d['result'] = 'nay'
    d['question'] = q.question .replace('<', '&lt;') .replace('>', '&gt;') .replace('[cpp]', '<pre class="sh_cpp">') .replace('[/cpp]', '</pre>')
    return render_to_response('quiz/index.html',
        d,
        context_instance=RequestContext(request)
        )
