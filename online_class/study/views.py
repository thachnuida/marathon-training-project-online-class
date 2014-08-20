from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from class_management.forms import *
from class_management.models import *
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils import simplejson
from study.models import *
import socket
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@login_required(login_url='/home/')
def study(request):
    userusing = request.user
    all_class = Class.objects.filter(students_in_class=userusing)
    paginator = Paginator(all_class, 10) # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        all_class = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_class = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_class = paginator.page(paginator.num_pages)
    return render(request, "study/study.html", {'all_class':all_class})

@login_required(login_url='/home/')
def lesson(request,class_id,pke):
    chosen_class = get_object_or_404(Class, pk=class_id)
    chosen_lesson = get_object_or_404(Lesson, pk=pke)
    all_test = chosen_lesson.test_set.all()
    paginator = Paginator(all_test, 16) # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        all_test = paginator.page(page)
    except PageNotAnInteger:
        all_test = paginator.page(1)
    except EmptyPage:
        all_test = paginator.page(paginator.num_pages)
    return render(request,"study/lesson.html",{
        'chosen_class':chosen_class,
        'chosen_lesson':chosen_lesson,
        'all_test':all_test,
        })

array_user_choose = []
@login_required(login_url='/home/')
def test(request,class_id,lesson_id,pk):
    global array_user_choose
    array_user_choose = []
    chosen_class  = get_object_or_404 (Class,pk=class_id)
    chosen_lesson = get_object_or_404 (Lesson,pk=lesson_id)
    chosen_test   = get_object_or_404 (Test,pk=pk)
    none_question = False
    try: 
        one_question = Question.objects.get(test=chosen_test, order_test=1)
        return render(request,"study/test.html",{
        'none_question':none_question,
        'one_question':one_question,
        'chosen_class':chosen_class,
        'chosen_lesson':chosen_lesson,
        'chosen_test':chosen_test
        })
    except:
        none_question = True
        return render(request,"study/test.html",{
            'none_question':none_question,
            'chosen_class':chosen_class,
            'chosen_lesson':chosen_lesson,
            'chosen_test':chosen_test
        })
    
import json

@login_required(login_url='/home/')
def question(request, test_id):
    global array_user_choose
    if request.method == "POST":
        current_order = int(request.POST['number'])
        order_test  = current_order+1
        if request.is_ajax():
            all_question2 = Question.objects.filter(test=test_id)
            lenght_question= len(all_question2)   
            question_id = request.POST['question_id']
            answer_user = request.POST['answer']

            if order_test <= lenght_question:
                if len(array_user_choose) >= current_order:
                    array_user_choose[current_order - 1] = answer_user  
                else:
                    array_user_choose += answer_user
                nextquestion = Question.objects.get(test=test_id, order_test=order_test)
                load = nextquestion.__dict__
                del load['_state']
                del load['right_answer']
                load['lenght']=lenght_question
                if load['image_ques'] != "":
                    load['image_ques'] = nextquestion.image_ques.url
                if order_test <= len(array_user_choose):
                    load['next_answer'] = array_user_choose[order_test - 1]
                else:
                    load['next_answer'] = ""
                topic_list = json.dumps({'load':load,'array_user_choose':array_user_choose})
                return HttpResponse(topic_list)
            else:
                load = {}
                load['lenght']=lenght_question
                load['order_test']=order_test
                if len(array_user_choose) >= current_order:
                    array_user_choose[current_order - 1] = answer_user  
                else:
                    array_user_choose += answer_user
                topic_list = json.dumps({
                    'load':load,'array_user_choose':array_user_choose
                    })
                return HttpResponse(topic_list)
        else:
            HttpResponse("aaa")            
    return HttpResponse("aaa")

@login_required(login_url='/home/')
def questionback(request, test_id):
    global array_user_choose
    if request.method == "POST":
        current_order  = int(request.POST['number'])
        order_test  = int(request.POST['number']) - 1
        if request.is_ajax():
            all_question2 = Question.objects.filter(test=test_id)
            lenght_question= len(all_question2)   
            question_id = request.POST['question_id']
            if 'answer' in request.POST:
                answer_user = request.POST['answer']
                if len(array_user_choose) >= current_order:
                        array_user_choose[current_order - 1] = answer_user  
                        print array_user_choose
                else:
                    array_user_choose += answer_user
                    print array_user_choose 
            previousquestion = Question.objects.get(test=test_id, order_test=order_test)
            load = previousquestion.__dict__
            del load['_state']
            del load['right_answer']
            load['lenght']=lenght_question
            load['previous_answer'] = array_user_choose[order_test - 1]
            if load['image_ques'] != "":
                load['image_ques'] = previousquestion.image_ques.url
            topic_list = json.dumps({'load':load,'array_user_choose':array_user_choose})
            return HttpResponse(topic_list)
        else:
            HttpResponse("aaa")            
    return HttpResponse("aaa")

@login_required(login_url='/home/')
def result(request,class_id,lesson_id,test_id):
    global array_user_choose
    chosen_class  = get_object_or_404 (Class,pk=class_id)
    chosen_lesson = get_object_or_404 (Lesson,pk=lesson_id)
    chosen_test = get_object_or_404 (Test,pk=test_id)
    list_right_answer = Question.objects.filter(test=test_id).order_by('order_test').values_list('right_answer', flat=True)
    all_question = Question.objects.filter(test=test_id)
    score=0
    for x, y in zip(array_user_choose, list_right_answer):
        if x == y:
            score+=1
    userusing = request.user
    score_user  = Score()
    score_user.user = request.user
    score_user.test = Test.objects.get(id=test_id)
    score_user.score = score
    score_user.save()

    return render(request,"study/result.html",{
        'score':score,
        'chosen_class':chosen_class,
        'chosen_lesson':chosen_lesson,
        'chosen_test':chosen_test,
        'all_question':all_question,
        'list_right_answer':list_right_answer,
        'answer_user':array_user_choose
        })

def leave_class(request, class_id):
    join_class = Class.objects.get(pk=class_id)
    join_class.students_in_class.remove(request.user)
    all_class = Class.objects.filter(students_in_class=request.user)
    paginator = Paginator(all_class, 10) # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        all_class = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_class = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_class = paginator.page(paginator.num_pages)
    return render(request, "study/study.html", {'all_class':all_class})

def studyclass(request,pk):
    join_class = get_object_or_404(Class,pk=pk)
    all_lesson = Lesson.objects.filter(Class=pk)
    all_student= len(join_class.students_in_class.all())
    quantity=Class.objects.filter(pk=pk).values_list('quantity', flat=True)

    canjoin=True
    if all_student>=quantity[0]:
        canjoin=False

    paginator = Paginator(all_lesson, 6) # Show 6 contacts per page
    page = request.GET.get('page')
    try:
        all_lesson = paginator.page(page)
    except PageNotAnInteger:
        all_lesson = paginator.page(1)
    except EmptyPage:
        all_lesson = paginator.page(paginator.num_pages)

    leave=False
    joined = True
    if request.user.is_anonymous():
        joined = False
    else:
        try:
            Class.objects.get(pk=pk, students_in_class=request.user)
            joined=True
        except: 
            joined = False
    if request.method == 'POST':
        if "join" in request.POST:
            join_class.students_in_class.add(request.user)
            joined = True
        if "leave" in request.POST:
            join_class.students_in_class.remove(request.user)
            joined = False
            leave = True

    return render(request, "study/studyclass.html", {
        'join_class':join_class,
        'all_lesson':all_lesson,
        'joined':joined,
        'leave':leave,
        'canjoin':canjoin
        })    
