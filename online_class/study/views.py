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
    chosen_test = Test.objects.all()

    all_lesson = Lesson.objects.filter(pk=pke)
    return render(request,"study/lesson.html",{
        'chosen_class':chosen_class,
        'chosen_lesson':chosen_lesson,
        'all_lesson':all_lesson,
        'chosen_test':chosen_test
        })


def test(request,class_id,lesson_id,pk):

    all_question = Question.objects.all()
    print all_question
    return render(request,"study/test.html",{
        'all_question':all_question
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

        print "Da tham gia"

    return render(request, "study/joinclass.html", {
        'all_lesson':all_lesson,
        'joined':joined
        })    
    