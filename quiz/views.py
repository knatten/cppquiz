import difflib
import random

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.mail import mail_admins
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.views.decorators.cache import never_cache

from quiz import fixed_quiz
from quiz.forms import QuestionForm
from quiz.game_data import *
from quiz.quiz_in_progress import *
from quiz.util import get_published_questions


@never_cache
def index(request):
    return random_question(request)


@never_cache
def random_question(request):
    try:
        return HttpResponseRedirect(
            "/quiz/question/%d" % get_unanswered_question(UserData(request.session)))
    except NoQuestionsExist:
        return HttpResponseRedirect("/quiz/no_questions")


@never_cache
def clear(request):
    user_data = UserData(request.session)
    request.session.clear()
    user_data.clear_correct_answers()
    save_user_data(user_data, request.session)
    return random_question(request)


@staff_member_required
def categorize(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('difficulty_'):
                pk = key.split('_')[1]
                q = Question.objects.get(pk=pk)
                q.difficulty = value
                anchor = "#question_%d" % q.pk
                q.save()
                return HttpResponseRedirect("/quiz/categorize/?changed=%d#question_%d" % (q.pk, q.pk))
    else:
        changed = int(request.GET.get('changed', 0))
        questions = get_published_questions().order_by('difficulty').annotate(num_answers=Count('usersanswer'))
        for q in questions:
            num_correct = len(UsersAnswer.objects.filter(question=q, correct=True))
            q.percentage_correct = num_correct * 100.0 / q.num_answers if q.num_answers > 0 else 0
        return render(request, 'quiz/categorize.html',
                      {'questions': questions, 'changed': changed})


def create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            mail_admins('Someone made a question!', 'https://' + request.get_host() + '/admin/quiz/question/?state=NEW')
            return HttpResponseRedirect('/quiz/created')
    else:
        form = QuestionForm()
    return render(request, 'quiz/create.html',
                  {'form': form, 'title': 'Create question'})


def preview_with_key(request, question_id):
    key = request.GET.get('preview_key')
    d = {}
    d['question'] = get_object_or_404(Question, id=question_id, preview_key=key)
    return render(request, 'quiz/preview.html', d)


def question(request, question_id):
    if request.GET.get('preview_key'):
        return preview_with_key(request, question_id)

    try:
        q = Question.objects.get(Q(id=question_id), Q(state='PUB') | Q(state='RET'))
    except Question.DoesNotExist:
        return render(request, 'quiz/missing_question.html', {'question_id': question_id}, status=404)

    user_data = UserData(request.session)
    q.mark_viewed()
    d = {}
    d['answered'] = False
    d['question'] = q
    d['dismissed_training_msg'] = user_data.dismissed_training_msg
    if request.GET.get('did_answer'):
        d['answered'] = True
        answer = Answer(q, request)
        answer.register_given_answer()
        user_data.register_attempt(answer)
        if answer.correct:
            d['correct_result'] = True
            user_data.register_correct_answer(question_id)
    d['total_questions'] = get_published_questions().count()
    d['user_data'] = user_data
    d['show_hint'] = request.GET.get('show_hint', False)
    d['title'] = ' - Question #%d' % q.pk
    d['attempts_required'] = max(0, 3 - user_data.attempts_given_for(question_id))
    save_user_data(user_data, request.session)
    return render(request, 'quiz/index.html', d)


def giveup(request, question_id):
    user_data = UserData(request.session)
    if user_data.attempts_given_for(question_id) < 3:
        raise Http404
    d = {}
    d['question'] = get_object_or_404(Question, id=question_id)
    return render(request, 'quiz/giveup.html', d)


@never_cache
def start(request):
    clear_quiz_in_progress(request.session)
    key = fixed_quiz.create_quiz()
    return HttpResponseRedirect('/q/%s' % key)


@never_cache
def quiz(request, quiz_key):
    d = {}
    try:
        quiz = Quiz.objects.get(key=quiz_key)
    except Quiz.DoesNotExist:
        return suggest_quiz_similar_to(quiz_key, request)
    quiz_in_progress = QuizInProgress(request.session, quiz)
    if request.GET.get('did_answer'):
        quiz_in_progress.answer(request)
        quiz_in_progress.save()
        return HttpResponseRedirect('/q/%s' % quiz_key)
    d['quiz_in_progress'] = quiz_in_progress
    if 'skip' in request.GET:
        quiz_in_progress.skip(request)
    if 'hint' in request.GET:
        quiz_in_progress.use_hint()
        d['hint'] = True
    if quiz_in_progress.is_finished(request):
        return render(request, 'quiz/finished.html', d)
    d['question'] = quiz_in_progress.get_current_question()
    d['question'].mark_viewed()
    d['title'] = ' - Quiz "' + quiz_key + '"'
    quiz_in_progress.save()
    return render(request, 'quiz/quiz.html', d)


def suggest_quiz_similar_to(key, request):
    suggestions = reversed(sorted(
        [(difflib.SequenceMatcher(None, q.key, key).ratio(), q.key)
         for q in Quiz.objects.all()]
    )[-5:])
    d = {
        'key': key,
        'suggestions': suggestions,
    }
    return render(request, 'quiz/suggest.html', d)


def dismiss_training_msg(request):
    user_data = UserData(request.session)
    user_data.dismiss_training_msg()
    save_user_data(user_data, request.session)
    return HttpResponse('')


def get_unanswered_question(user_data):
    # TODO what if there are no questions
    available_questions = [q.id for q in get_published_questions()]
    if len(available_questions) == 0:
        raise NoQuestionsExist
    for q in user_data.get_correctly_answered_questions():
        if int(q) in available_questions:
            available_questions.remove(int(q))
    if len(available_questions) == 0:
        return get_published_questions().order_by('?')[0].id
    else:
        return random.choice(available_questions)


def raise_exception(request):
    raise Exception("Test exception raised")


class NoQuestionsExist(Exception):
    pass
