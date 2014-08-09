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
# Create your views here.

def study(request):
    userusing = request.user
    # join_class = get_object_or_404(Class,pk=pk)
    # student_list = join_class.students_in_class.all()
    # print student_list
    user=User.objects.filter(username="student1")
    class1=Class.objects.filter(students_in_class=user)
    all_class = Class.objects.filter(students_in_class=userusing)
    return render(request, "study/study.html", {'all_class':all_class})

@login_required
def studyclass(request,pk):
    join_class = get_object_or_404(Class,pk=pk)
    all_lesson = Lesson.objects.filter(Class=pk)
    userusing = request.user

    # join_class.students_in_class.add(user_using)

    joined = True
    if request.method == 'POST':
        join_class.students_in_class.remove(userusing)
        joined = False
    return render(request, "study/studyclass.html" ,{
        'all_lesson':all_lesson,
        'join_class':join_class,
        'joined':joined
        })

def lesson(request,class_id,pke):
    chosen_class = get_object_or_404(Class, pk=class_id)
    chosen_lesson = get_object_or_404(Lesson, pk=pke)
    chosen_test = chosen_lesson.test_set.all()

    all_lesson = Lesson.objects.filter(pk=pke)
    return render(request,"study/lesson.html",{
        'chosen_class':chosen_class,
        'chosen_lesson':chosen_lesson,
        'all_lesson':all_lesson,
        'chosen_test':chosen_test
        })


def test(request,class_id,lesson_id,pk):
    chosen_class  = get_object_or_404 (Class,pk=class_id)
    chosen_lesson = get_object_or_404 (Lesson,pk=lesson_id)
    chosen_test   = get_object_or_404 (Test,pk=pk)  
    # all_question1  = chosen_test.question_set.all()
    # one_question1 = Question.objects.filter(test=pk).values_list('id', flat=True).order_by('id')
    # one_question2 = Question.objects.filter(test=pk).values_list('right_answer', flat=True)
    one_question = Question.objects.get(test=chosen_test, order_test=1)



    return render(request,"study/test.html",{
        'one_question':one_question,
        'chosen_class':chosen_class,
        'chosen_lesson':chosen_lesson,
        'chosen_test':chosen_test
        })
    
import json
def question(request, test_id):
    score=0
    if request.method == "POST":
        all_question2 = Question.objects.filter(test=test_id)
        lenght_question= len(all_question2)
      
        order_test  = int(request.POST['number'])
        question_id = request.POST['question_id']
        answer_user = request.POST['answer']
        if order_test==1:
            array_user_choose=[]
            array_user_choose.append(answer_user)
            print type (array_user_choose)
            print type (answer_user)
            print "lan so 1"
        elif order_test<=lenght_question:
            array_user_choose=request.POST['answer_user']
            array_user_choose+=answer_user
            # array_user_choose.append(answer_user)
            print (array_user_choose)
            print type (array_user_choose)
            # array_user_choose[question_id]=answer_user
            print "lan so 2"            
        if order_test < lenght_question:          
            order_test+=1    
            # one_right_answer = Question.objects.filter(test=test_id,id=question_id).values_list('right_answer', flat=True)
            nextquestion = Question.objects.get(test=test_id, order_test=order_test)
            print type(nextquestion)
            load = nextquestion.__dict__
            del load['_state']
            del load['right_answer']
            load['lenght']=lenght_question
            if load['image_ques'] != "":
                load['image_ques'] = nextquestion.image_ques.url
            topic_list = json.dumps({'load':load,'array_user_choose':array_user_choose})
            return HttpResponse(topic_list)
        else:
            jsaction = 'window.location.pathname="study/result.html"'
            topic_list = json.dumps({
                'array_user_choose':array_user_choose,
                'jsaction':jsaction
                })
            return HttpResponse(topic_list)      
    return HttpResponse("aaa")

def result(request,class_id,lesson_id,test_id):
    chosen_class  = get_object_or_404 (Class,pk=class_id)
    chosen_lesson = get_object_or_404 (Lesson,pk=lesson_id)
    chosen_test = get_object_or_404 (Test,pk=test_id)

    answer_user=request.POST['answer_user'] 

    print " ket qua cua ng tra loi"
    print answer_user
    list_right_answer = Question.objects.filter(test=test_id).values_list('right_answer', flat=True)
    all_question = Question.objects.filter(test=test_id)

    # print array_user_choose
    # print answer_user
    a=test_id
    print "aaaa"
    print a
    score=0
    
    print "result"
    ab="AAAAA"
    print list_right_answer
    # [x==y for x, y in zip(a, one_right_answer)]
    for x, y in zip(answer_user, list_right_answer):
        if x == y:
            score+=10
            print "score"
            print score

    userusing = request.user
    try:
        score_user = Score.objects.get(id=test_id)
        score_user.score=score
        score_user.save(update_fields=['score'])
        print " co ton tai"

    except Score.DoesNotExist:
        print " k ton tai"  
        score_user  = Score()
        score_user.useru=User.objects.get(username=userusing)
        score_user.test=Test.objects.get(id=test_id)
        score_user.score=score
        score_user.save()

    return render(request,"study/result.html",{
        'score':score,
        'chosen_class':chosen_class,
        'chosen_lesson':chosen_lesson,
        'chosen_test':chosen_test,
        'all_question':all_question,
        'list_right_answer':list_right_answer,
        'answer_user':answer_user
        })


def join(request):    
    all_class1 = Class.objects.all()
    # chosen_class=get_object_or_404(Class,pk=pk)
    userusing = request.user
    all_class=all_class1.exclude(students_in_class=userusing)
    # chosen_class.students_in_class.add(user_using)
    return render(request, "study/join.html", {'all_class':all_class})

def joinclass(request,pk):
    join_class = get_object_or_404(Class,pk=pk)
    all_lesson = Lesson.objects.filter(Class=pk)
    user_using = request.user

    joined = True

    if request.method == 'POST':
        join_class.students_in_class.add(user_using)
        joined = False


    return render(request, "study/joinclass.html", {
        'join_class':join_class,
        'all_lesson':all_lesson,
        'joined':joined
        })    