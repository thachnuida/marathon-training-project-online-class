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
from django.db.models import Count
from study.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test, login_required


# Create your views here.

def check_teacher(user):
    return "T" in user.userprofile.role

@user_passes_test(check_teacher, login_url='/home/')
def classlist(request):
    teacher = request.user
    ones_classes = Class.objects.filter(teacher = teacher)
    paginator = Paginator(ones_classes, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        ones_classes = paginator.page(page)
    except PageNotAnInteger:
        ones_classes = paginator.page(1)
    except EmptyPage:
        ones_classes = paginator.page(paginator.num_pages)

    return render(request, "class_management/ones_classes.html", {'ones_classes':ones_classes})

@user_passes_test(check_teacher, login_url='/home/')
def create_class(request):
    form = CreateClass()
    if request.method == 'POST':
        form = CreateClass(request.POST, request.FILES)
        if form.is_valid():
            if (UserProfile.objects.get(user=request.user).role == 'T'):
                createdclass = Class(class_name = form.cleaned_data['class_name'], teacher = request.user, quantity = form.cleaned_data['quantity'], image_class=form.cleaned_data['image_class'], description=request.POST['description'], enable='T')
                createdclass.save()
                return HttpResponseRedirect(reverse('classes:classlist'))
            else :
                form
        else :
            form
    return render(request, "class_management/create_class.html", {'form':form})

@user_passes_test(check_teacher, login_url='/home/')
def detail_class(request, pk):
    Chose_class = get_object_or_404(Class, pk=pk)
    lesson_list = Chose_class.lesson_set.all()
    paginator = Paginator(lesson_list, 6) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        lesson_list = paginator.page(page)
    except PageNotAnInteger:
        lesson_list = paginator.page(1)
    except EmptyPage:
        lesson_list = paginator.page(paginator.num_pages)
    if Chose_class.image_class:
        form = CreateClass(class_details=Chose_class.__dict__, image_url=Chose_class.image_class.url)
    else:
        form = CreateClass(class_details=Chose_class.__dict__)
    if request.method == 'POST':
        form = CreateClass(request.POST, request.FILES)
        if form.is_valid():
            Class.objects.filter(pk=pk).update(class_name = form.cleaned_data['class_name'], teacher = request.user, quantity = form.cleaned_data['quantity'], description=request.POST['description'])
            updatedclass = get_object_or_404(Class, pk = pk)
            if form.cleaned_data['image_class'] != None:
                updatedclass.image_class = form.cleaned_data['image_class']
            updatedclass.save()
            return HttpResponseRedirect(reverse('classes:detailclass', args=[pk]))
    return render(request, "class_management/detail_class.html", {"form": form, 'Chose_class':Chose_class, 'lesson_list':lesson_list })

@user_passes_test(check_teacher, login_url='/home/')
def disable_class(request, class_id):
    if Class.objects.get(pk=class_id).enable == 'T':
        Class.objects.filter(pk=class_id).update(enable='F')
    else:
        Class.objects.filter(pk=class_id).update(enable='T')
    return HttpResponseRedirect(reverse('classes:classlist'))

@user_passes_test(check_teacher, login_url='/home/')
def create_lesson(request, class_id):
    chosen_class = Class.objects.get(pk=class_id)
    form = CreateLesson()
    if request.method == 'POST':
        form=CreateLesson(request.POST)
        if form.is_valid():
            createdlesson = Lesson(lesson_name = form.cleaned_data['lesson_name'], Class = Class.objects.get(pk=class_id), description=form.cleaned_data['description'], video_link = form.cleaned_data['video_link'])
            createdlesson.save()
            return HttpResponseRedirect(reverse('classes:detailclass', args=[class_id]))
    return render(request, "class_management/create_lesson.html", {'form':form, 'chosen_class':chosen_class})

@user_passes_test(check_teacher, login_url='/home/')
def delete_lesson(request, class_id, pk):
    Lesson.objects.get(Class=class_id, pk=pk).delete()
    return HttpResponseRedirect(reverse('classes:detailclass', args=[class_id]))

@user_passes_test(check_teacher, login_url='/home/')
def detail_lesson(request, class_id, pk):
    chosen_lesson = get_object_or_404(Lesson, pk=pk)
    chosen_class = get_object_or_404(Class, pk=class_id)
    test_list = chosen_lesson.test_set.all()
    paginator = Paginator(test_list, 24) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        test_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        test_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        test_list = paginator.page(paginator.num_pages)
    form = CreateLesson(chosen_lesson=chosen_lesson.__dict__)
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
    return render(request, "class_management/detail_lesson.html", {"form": form, 'chosen_lesson':chosen_lesson, 'test_list':test_list, 'formtest':formtest, 'chosen_class':chosen_class})

@user_passes_test(check_teacher, login_url='/home/')     
def student_class(request, pk):
    chosen_class = get_object_or_404(Class, pk=pk)
    student_list = chosen_class.students_in_class.all()
    paginator = Paginator(student_list, 25) # Show 25 per page
    page = request.GET.get('page')
    try:
        student_list = paginator.page(page)
    except PageNotAnInteger:
        student_list = paginator.page(1)
    except EmptyPage:
        student_list = paginator.page(paginator.num_pages)

    chart = []
    for student in student_list:
        chart.append(calpercent(chosen_class, student))
    return render(request, "class_management/student_class.html", {'chosen_class':chosen_class, 'student_list':student_list, 'chart': chart})

@login_required(login_url='/home/')
def student_process(request, user_id):
    user = User.objects.get(pk=user_id)
    class_list = Class.objects.filter(students_in_class=user_id)
    paginator = Paginator(class_list, 10) # Show 25 per page
    page = request.GET.get('page')
    try:
        class_list = paginator.page(page)
    except PageNotAnInteger:
        class_list = paginator.page(1)
    except EmptyPage:
        class_list = paginator.page(paginator.num_pages)

    chart = []
    for class_item in class_list:
        chart.append(calpercent(class_item, user))
    return render(request, "class_management/student_process.html", {'user':user, 'class_list': class_list, 'chart':chart })


def calpercent(chosen_class, user):
    num_test = Test.objects.filter(lesson__Class=chosen_class).count()
    test_list = Test.objects.filter(lesson__Class=chosen_class)
    non_test = 0
    good_test = 0
    medium_test = 0
    bad_test = 0
    for test in test_list:
        question_num = Question.objects.filter(test=test).count()
        score = Score.objects.filter(test=test, user=user).aggregate(Max('score'))['score__max']
        print score
        print float(question_num*70)/100
        if score != None:
            if float(score) >= float(question_num*70)/100:
                good_test += 1
            if score < float(question_num*70)/100 and score >= float(question_num*50)/100:
                medium_test += 1
            if score < float(question_num*50)/100:
                bad_test += 1
        else:
            non_test += 1
    chart = [[[0, good_test]], [[0, medium_test]], [[0,bad_test]], [[0,non_test]], num_test ]
    return chart

from django.utils import simplejson
from django.db.models import Max

@user_passes_test(check_teacher, login_url='/home/')  
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
    return render(request, "class_management/create_test.html", {"form": form,"chosen_class": chosen_class,"chosen_lesson":chosen_lesson, "chosen_test":chosen_test, "question_list":question_list})

@user_passes_test(check_teacher, login_url='/home/')  
def delete_test(request, class_id, lesson_id, pk):
    Test.objects.filter(lesson=lesson_id, pk=pk).delete();
    return HttpResponseRedirect(reverse('classes:detaillesson', args=[class_id, lesson_id]))

@user_passes_test(check_teacher, login_url='/home/')  
def detail_test(request, class_id, lesson_id, test_id):
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
    return render(request, "class_management/detail_test.html", {"form": form,"chosen_class": chosen_class,"chosen_lesson":chosen_lesson, "chosen_test":chosen_test, "question_list":question_list})
from django.views.decorators.csrf import csrf_protect

@user_passes_test(check_teacher, login_url='/home/')  
def update_question(request, test_id):
    chosen_test = get_object_or_404(Test, pk=test_id)
    if request.method == 'POST':
        if request.is_ajax():
            form = CreateQuestion(request.POST, request.FILES)
            if form.is_valid():
                id_question = request.POST['id']
                print form.cleaned_data['image_ques']
                Question.objects.filter(test=test_id, order_test=id_question).update(question = form.cleaned_data['question'], answerA = form.cleaned_data['answerA'], answerB = form.cleaned_data['answerB'], answerC = form.cleaned_data['answerC'], answerD = form.cleaned_data['answerD'], right_answer = form.cleaned_data['right_answer'])
                updatedquestion = get_object_or_404(Question, test=test_id, order_test = id_question)
                if form.cleaned_data['image_ques'] != None:
                    updatedquestion.image_ques = form.cleaned_data['image_ques']
                updatedquestion.save()
                question =Question.objects.get(test=test_id, order_test=id_question)
                question_dict = question.__dict__
                del question_dict['_state']
                if question_dict['image_ques'] != "":
                    question_dict['image_ques'] = question.image_ques.url
                print question_dict
                return HttpResponse(simplejson.dumps(question_dict))
            else :
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)
                return HttpResponseBadRequest(simplejson.dumps(errors_dict))
    return HttpResponse("never come");
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
@user_passes_test(check_teacher, login_url='/home/')  
def delete_question(request, test_id):
    if request.method == 'POST':
        if request.is_ajax():
            id_question = request.POST['id']
            order = Question.objects.filter(test=Test.objects.get(pk=test_id)).aggregate(Max('order_test'))
            order_test = order['order_test__max']
            Question.objects.filter(test=test_id, order_test=id_question).delete()
            i = int(id_question) + 1
            while (i <= int(order_test)):
                new_order = i - 1
                Question.objects.filter(test=test_id, order_test=i).update(order_test=new_order)
                i = i + 1
            return HttpResponse(simplejson.dumps({}))    
    return HttpResponse("never come");

from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
option = 'Default'
@login_required(login_url='/home/')  
def test_history(request, user_id, class_id):
    global option
    student = get_object_or_404(User, pk=user_id)
    chosen_class = Class.objects.get(pk=class_id)
    if request.method == 'POST':
        if request.is_ajax():
            response = []
            if request.POST['option'] == 'Lesson':
                option='Lesson'
                test_list = Score.objects.filter(user=student, test__lesson__Class=class_id).annotate(question_num=Count('test__question')).order_by('test__lesson')
            if request.POST['option'] == 'Score':
                option="Score"
                test_list = Score.objects.filter(user=student, test__lesson__Class=class_id).annotate(question_num=Count('test__question')).order_by('score')
            if request.POST['option'] == 'Time':
                option="Time"
                test_list = Score.objects.filter(user=student, test__lesson__Class=class_id).annotate(question_num=Count('test__question')).order_by('test_date')
            paginator = Paginator(test_list, 10) # Show 30 per page
            page = request.GET.get('page')
            try:
                test_list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                test_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                test_list = paginator.page(paginator.num_pages)
            html = "<table>"
            html = html + '<tr class="table_title">'
            html = html + '<th></th>'
            html = html + '<th>Your Score</th>'
            html = html + '<th>Doing Exercise Time</th>'
            html = html + '<th>Lesson Name</th>'
            html = html + '<th>Test Name</th>'
            html = html + '</tr>'
            for test in test_list:
                df = DateFormat(test.test_date)
                html = html + "<tr>"
                html = html + "<td class='time-period-left-blue'></td>"
                html = html + "<td>Score: "+ str(test.score) +"/"+ str(test.question_num)+ "</td>"
                html = html + "<td>"+ str(df.format('H:i d/m/Y'))+"</td>"
                html = html + "<td>"+ str(test.test.lesson)+"</td>"
                html = html + "<td>"+ str(test.test)+"</td>"
                html = html + "</tr>"
            html = html +"</table>"
            return HttpResponse(html)
    if option == 'Default':
        test_list = Score.objects.filter(user=student, test__lesson__Class=class_id).annotate(question_num=Count('test__question'))
    if option == 'Time':
        test_list = Score.objects.filter(user=student, test__lesson__Class=class_id).annotate(question_num=Count('test__question')).order_by('test_date')
    if option == 'Lesson':
        test_list = Score.objects.filter(user=student, test__lesson__Class=class_id).annotate(question_num=Count('test__question')).order_by('test__lesson')
    if option == 'Score':
        test_list = Score.objects.filter(user=student, test__lesson__Class=class_id).annotate(question_num=Count('test__question')).order_by('score')
    paginator = Paginator(test_list, 12) # Show 30 per page
    page = request.GET.get('page')
    try:
        test_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        test_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        test_list = paginator.page(paginator.num_pages)
    return render(request, "class_management/test_history.html", {'student': student,'test_list':test_list, 'chosen_class':chosen_class})

@user_passes_test(check_teacher, login_url='/home/')  
def student_detail(request, user_id):
    student = get_object_or_404(User,pk=user_id)
    class_list = Class.objects.filter(students_in_class=student)
    paginator = Paginator(class_list, 10) # Show 10 per page
    page = request.GET.get('page')
    try:
        class_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        class_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        class_list = paginator.page(paginator.num_pages)
    return render(request, "class_management/student_detail.html", {'student':student, 'class_list':class_list})