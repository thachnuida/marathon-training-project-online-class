from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from class_management.forms import *
from class_management.models import *

# Create your views here.
def classlist(request, teacher_id):
    ones_classes = Class.objects.filter(teacher__id = teacher_id)
    return render(request, "class_management/ones_classes.html", {'ones_classes':ones_classes})

# def create_class(request):
#     return render(request, "class_management/create_class.html")

def create_class(request):
    form = CreateClass()
    if request.method == 'POST':
        print 'Classname: ' + request.POST['class_name']
        print 'Slug: ' + request.POST['slug']
        print 'Quantity' + request.POST['quantity']
        # p = Book(title = request.POST['name'],desc= request.POST['desc'],publication_date = datetime.datetime.now())
        # p.save()
        # books = Book.objects.all()
        return render(request, "class_management/index.html")
    return render(request, "class_management/create_class.html", {'form':form})