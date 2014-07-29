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
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseBadRequest


# Create your views here.
def classlist(request):
    teacher = request.user
    ones_classes = Class.objects.filter(teacher = teacher)
    return render(request, "class_management/ones_classes.html", {'ones_classes':ones_classes})

def create_class(request):
    form = CreateClass()
    if request.method == 'POST':
        form = CreateClass(request.POST, request.FILES)

        if form.is_valid():
            if (UserProfile.objects.get(user=request.user).role == 'T'):
                createdclass = Class(class_name = form.cleaned_data['class_name'], teacher = request.user, quantity = form.cleaned_data['quantity'], image_class=form.cleaned_data['image_class'], description=request.POST['description'])
                createdclass.save()
                return HttpResponseRedirect(reverse('classes:classlist'))
            else :
                form
        else :
            form
    return render(request, "class_management/create_class.html", {'form':form})

def detail_class(request, pk):
    Chose_class = get_object_or_404(Class, pk=pk)
    lesson_list = Chose_class.lesson_set.all()
    if Chose_class.image_class:
        form = CreateClass(class_details=Chose_class.__dict__, image_url=Chose_class.image_class.url)
    else:
        form = CreateClass(class_details=Chose_class.__dict__)
    if request.method == 'POST':
        form = CreateClass(request.POST, request.FILES)
        if form.is_valid():
            Class.objects.filter(pk=pk).update(class_name = form.cleaned_data['class_name'], teacher = request.user, quantity = form.cleaned_data['quantity'], description=request.POST['description'])
            updatedclass = get_object_or_404(Class, pk = pk)
            updatedclass.image_class = form.cleaned_data['image_class']
            updatedclass.save()
            return HttpResponseRedirect(reverse('classes:detailclass', args=[pk]))
    return render(request, "class_management/detail_class.html", {"form": form, 'Chose_class':Chose_class, 'lesson_list':lesson_list })

def create_lesson(request, class_id):
    form = CreateLesson()
    if request.method == 'POST':
        form=CreateLesson(request.POST)
        if form.is_valid():
            createdlesson = Lesson(lesson_name = form.cleaned_data['lesson_name'], Class = Class.objects.get(pk=class_id), description=form.cleaned_data['description'], video_link = form.cleaned_data['video_link'])
            createdlesson.save()
            return HttpResponseRedirect(reverse('classes:detailclass', args=[class_id]))
    return render(request, "class_management/create_lesson.html", {'form':form })

def detail_lesson(request, class_id, pk):
    chose_lesson = get_object_or_404(Lesson, pk=pk)
    test_list = chose_lesson.test_set.all()
    form = CreateLesson(chose_lesson=chose_lesson.__dict__)
    formtest = CreateTest()
    if request.method == 'POST':
        if 'lesson' in request.POST:
            form = CreateLesson(request.POST)
            if form.is_valid():
                Lesson.objects.filter(pk=pk).update(lesson_name = form.cleaned_data['lesson_name'], description=form.cleaned_data['description'], video_link=form.cleaned_data['video_link'])
                return HttpResponseRedirect(reverse('classes:detaillesson', args=[class_id, pk]))
        if 'test' in request.POST:
            formtest = CreateTest(request.POST)
            if formtest.is_valid():
                test = Test(lesson = Lesson.objects.get(pk=pk), test_name = formtest.cleaned_data['test_name'])
                test.save()
                return HttpResponseRedirect(reverse('classes:createtest', args=[class_id, pk, test.id]))
    return render(request, "class_management/detail_lesson.html", {"form": form, 'chose_lesson':chose_lesson, 'test_list':test_list, 'formtest':formtest})
     
def studentclass(request, pk):
    chose_class = get_object_or_404(Class, pk=pk)
    student_list = chose_class.students_in_class.all()
    print calpercent(chose_class)
    chart = {"d1" : [[0,33]],  "d2" : [[0,44]],   "d3" : [[0,3]],    "d4" : [[0,30]]}
    return render(request, "class_management/studentclass.html", {'student_list':student_list, "chart":chart})

def calpercent(chose_class):
    lessons = chose_class.lesson_set.all()
    test_sum = 0
    for lesson in lessons:
        print lesson
        print test_sum
        test_sum += lesson.test_set.count()
    return test_sum

from django.utils import simplejson
from django.db.models import Max

def create_test(request, class_id, lesson_id, test_id):
    form = CreateQuestion()
    chosen_class = get_object_or_404(Class, pk=class_id)
    chosen_lesson = get_object_or_404(Lesson, pk=lesson_id)
    chosen_test = get_object_or_404(Test, pk=test_id)
    question_list = Question.objects.filter(test=Test.objects.get(pk=test_id))
    if request.method == 'POST':
        if request.is_ajax():
            form = CreateQuestion(request.POST, request.FILES)
            if form.is_valid():
                order = Question.objects.filter(test=Test.objects.get(pk=test_id)).aggregate(Max('order_test'))
                order_test = order['order_test__max']
                if order_test == None: 
                    order_test = 1
                else :
                    order_test = order_test + 1
                question = Question(test=Test.objects.get(pk=test_id), question = form.cleaned_data['question'], answerA = form.cleaned_data['answerA'], answerB = form.cleaned_data['answerB'], answerC = form.cleaned_data['answerC'], answerD = form.cleaned_data['answerD'], right_answer = form.cleaned_data['right_answer'], image_ques = form.cleaned_data['image_ques'], order_test = order_test)
                question.save()
                question =Question.objects.get(pk=question.pk)
                question_dict = question.__dict__
                del question_dict['_state']
                if question_dict['image_ques'] != "":
                    question_dict['image_ques'] = question.image_ques.url
                return HttpResponse(simplejson.dumps(question_dict))
            else :
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)
                return HttpResponseBadRequest(simplejson.dumps(errors_dict))
    return render(request, "class_management/questionintest.html", {"form": form,"chosen_class": chosen_class,"chosen_lesson":chosen_lesson, "chosen_test":chosen_test, "question_list":question_list})

