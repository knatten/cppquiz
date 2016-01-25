import difflib
import logging
import random

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import mail_admins
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count

import fixed_quiz
from models import *
from forms import QuestionForm
from answer import Answer
from game_data import *
from quiz_in_progress import *

def index(request):
    return random_question(request)

def random_question(request):
    try:
        return HttpResponseRedirect(
            "/quiz/question/%d" % get_unanswered_question(UserData(request.session)))
    except NoQuestionsExist:
        return HttpResponseRedirect("/quiz/no_questions")

def clear(request):
    user_data = UserData(request.session)
    request.session.clear()
    user_data.clear_correct_answers()
    save_user_data(user_data, request.session)
    return random_question(request)

@staff_member_required
def categorize(request):
    if request.method == 'POST':
        for key, value in request.POST.iteritems():
            if key.startswith('difficulty_'):
                pk = key.split('_')[1]
                q = Question.objects.get(pk=pk)
                q.difficulty = value
                anchor = "#question_%d" % q.pk
                q.save()
                return HttpResponseRedirect("/quiz/categorize/?changed=%d#question_%d" % (q.pk, q.pk))
    else:
        changed = int(request.REQUEST.get('changed', 0))
        questions = Question.objects.filter(published=True).order_by('difficulty')\
                    .annotate(num_answers=Count('usersanswer'))
        for q in questions:
            num_correct = len(UsersAnswer.objects.filter(question=q, correct=True))
            q.percentage_correct = num_correct * 100.0 / q.num_answers
        return render_to_response('quiz/categorize.html' ,
            {'questions': questions, 'changed':changed},
            context_instance=RequestContext(request)
            )

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
        {'form':form, 'title':'Create question'},
        context_instance=RequestContext(request)
        )

def preview(request, question_id):
    if not request.user.is_staff:
        raise Http404
    d = {}
    d['question'] = get_object_or_404(Question, id=question_id)
    return render_to_response('quiz/preview.html',
        d,
        context_instance=RequestContext(request)
        )

def preview_with_key(request, question_id):
    key = request.REQUEST.get('preview_key')
    d = {}
    d['question'] = get_object_or_404(Question, id=question_id, preview_key=key)
    return render_to_response('quiz/preview.html',
        d,
        context_instance=RequestContext(request)
        )

def question(request, question_id):
    if request.REQUEST.get('preview'):
        return preview(request, question_id)
    if request.REQUEST.get('preview_key'):
        return preview_with_key(request, question_id)
    user_data = UserData(request.session)
    q = get_object_or_404(Question, id=question_id, published=True)
    d = {}
    d['answered'] = False
    d['question'] = q
    d['dismissed_training_msg'] = user_data.dismissed_training_msg
    if request.REQUEST.get('did_answer'):
        d['answered'] = True
        answer = Answer(q, request)
        answer.register_given_answer()
        user_data.register_attempt(answer)
        if answer.correct:
            d['correct_result'] = True
            user_data.register_correct_answer(question_id)
    d['total_questions'] = Question.objects.filter(published=True).count()
    d['user_data'] = user_data
    d['show_hint'] = request.REQUEST.get('show_hint', False)
    d['title'] = ' - Question #%d' % q.pk
    d['attempts_required'] = max(0, 3 - user_data.attempts_given_for(question_id))
    save_user_data(user_data, request.session)
    return render_to_response('quiz/index.html',
        d,
        context_instance=RequestContext(request)
        )

def giveup(request, question_id):
    user_data = UserData(request.session)
    if user_data.attempts_given_for(question_id) < 3:
        raise Http404
    d = {}
    d['question'] = get_object_or_404(Question, id=question_id)
    return render_to_response('quiz/giveup.html',
        d,
        context_instance=RequestContext(request)
        )

def start(request):
    clear_quiz_in_progress(request.session)
    key = fixed_quiz.create_quiz()
    return HttpResponseRedirect('/q/%s' % key)


def quiz(request, quiz_key):
    d = {}
    try:
        quiz = Quiz.objects.get(key=quiz_key)
    except Quiz.DoesNotExist:
        return suggest_quiz_similar_to(quiz_key, request)
    quiz_in_progress = QuizInProgress(request.session, quiz)
    if request.REQUEST.get('did_answer'):
        quiz_in_progress.answer(request)
        quiz_in_progress.save()
        return HttpResponseRedirect('/q/%s' % quiz_key)
    d['quiz_in_progress'] = quiz_in_progress
    if request.GET.has_key('skip'):
        quiz_in_progress.skip(request)
    if request.GET.has_key('hint'):
        quiz_in_progress.use_hint()
        d['hint'] = True
    if quiz_in_progress.is_finished(request):
        debug_string = "IP:%s, quiz:%s was served the finished-screen " % (util.get_client_ip(request), quiz_in_progress.quiz.key)
        logging.getLogger('quiz').debug(debug_string)
        return render_to_response('quiz/finished.html',
            d,
            context_instance=RequestContext(request)
            )
    d['question'] = quiz_in_progress.get_current_question()
    d['title'] = ' - Quiz "' + quiz_key + '"'
    quiz_in_progress.save()
    return render_to_response('quiz/quiz.html',
        d,
        context_instance=RequestContext(request)
        )

def suggest_quiz_similar_to(key, request):
    suggestions = reversed(sorted(
            [(difflib.SequenceMatcher(None, q.key, key).ratio(), q.key)
                for q in Quiz.objects.all()]
                    )[-5:])
    d = {
        'key': key,
        'suggestions': suggestions,
    }
    return render_to_response('quiz/suggest.html',
        d,
        context_instance=RequestContext(request)
        )

def dismiss_training_msg(request):
    user_data = UserData(request.session)
    user_data.dismiss_training_msg()
    save_user_data(user_data, request.session)
    return HttpResponse('')

#TODO what if there are no questions
def get_unanswered_question(user_data):
    available_questions = [q.id for q in Question.objects.filter(published=True)]
    if len(available_questions) == 0:
        raise NoQuestionsExist
    for q in user_data.get_correctly_answered_questions():
        if int(q) in available_questions:
            available_questions.remove(int(q))
    if len(available_questions) == 0:
        return Question.objects.filter(published=True).order_by('?')[0].id
    else:
        return random.choice(available_questions)

def raise_exception(request):
    raise Exception("Test exception raised")

class NoQuestionsExist(Exception):
    pass
