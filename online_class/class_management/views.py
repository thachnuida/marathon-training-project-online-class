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
    if request.method == 'POST':
        form = CreateLesson(request.POST)
        if form.is_valid():
            Lesson.objects.filter(pk=pk).update(lesson_name = form.cleaned_data['lesson_name'], description=form.cleaned_data['description'], video_link=form.cleaned_data['video_link'])
            return HttpResponseRedirect(reverse('classes:detaillesson', args=[class_id, pk]))
    return render(request, "class_management/detail_lesson.html", {"form": form, 'chose_lesson':chose_lesson, 'test_list':test_list})

def create_test(request, class_id, lesson_id):
    # if request.method == 'POST':
    #     form=CreateLesson(request.POST)
    #     if form.is_valid():
    #         createdlesson = Lesson(lesson_name = form.cleaned_data['lesson_name'], Class = Class.objects.get(pk=class_id), description=form.cleaned_data['description'], video_link = form.cleaned_data['video_link'])
    #         createdlesson.save()
    #         return HttpResponseRedirect(reverse('classes:detailclass', args=[class_id]))
    return render(request, "class_management/create_test.html")

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