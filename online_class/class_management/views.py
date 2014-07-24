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
    print UserProfile.objects.get(user=request.user).role
    teacher = request.user
    ones_classes = Class.objects.filter(teacher = teacher)
    return render(request, "class_management/ones_classes.html", {'ones_classes':ones_classes})
# def create_class(request):
#     return render(request, "class_management/create_class.html")

def create_class(request):
    form = CreateClass()
    if request.method == 'POST':
        form = CreateClass(request.POST, request.FILES)
        if form.is_valid():
            if (UserProfile.objects.get(user=request.user).role == 'T'):
                createdclass = Class(class_name = form.cleaned_data['class_name'], teacher = request.user,slug=slugify(form.cleaned_data['class_name']), quantity = form.cleaned_data['quantity'], image_class=form.cleaned_data['image_class'], description=request.POST['description'])
                createdclass.save()
                return HttpResponseRedirect(reverse('classes:classlist'))
            else :
                form
        else :
            form
    return render(request, "class_management/create_class.html", {'form':form})

def detailclass(request, pk):
    Chose_class = get_object_or_404(Class, pk=pk)
    form = CreateClass(class_details=Chose_class.__dict__)
    if request.method == 'POST':
        form = CreateClass(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['image_class'] == None:
                print "one"
            else :
                print "two"
            # Class.objects.filter(pk=pk).update(class_name = form.cleaned_data['class_name'], teacher = request.user,slug=slugify(form.cleaned_data['class_name']), quantity = form.cleaned_data['quantity'], image_class=form.cleaned_data['image_class'], description=request.POST['description'])
            # createdclass = Class(class_name = form.cleaned_data['class_name'], teacher = request.user,slug=slugify(form.cleaned_data['class_name']), quantity = form.cleaned_data['quantity'], image_class=form.cleaned_data['image_class'], description=request.POST['description'])
            # createdclass.save()
            return HttpResponseRedirect(reverse('classes:classlist'))
        else :
            form
    return render(request, "class_management/detailclass.html", {"form": form, 'Chose_class':Chose_class})

def studentclass(request, pk):
    return render(request, "class_management/studentclass.html")

# class detailclass():
#     model = Class
#     template_name = 'class_management/detailclass.html'