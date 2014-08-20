from django.shortcuts import *
from home.forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from class_management.models import *
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.

def register(request):
    registered=False
    if request.method =='POST':
        user_form=UserForm(data=request.POST) 
        profile_form=UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'user_image' in request.FILES:
                profile.user_image = request.FILES['user_image']
            profile.save()
            registered = True
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home:home'))
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
    return render(request,
            'home/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

from django.utils import simplejson
from django.core import serializers
def home(request):
    all_class = Class.objects.filter(enable="T")
    paginator = Paginator(all_class, 8) # Show 8 contacts per page
    page = request.GET.get('page')
    try:
        all_class = paginator.page(page)
    except PageNotAnInteger:
        all_class = paginator.page(1)
    except EmptyPage:
        all_class = paginator.page(paginator.num_pages)

    recently_class = Class.objects.filter(enable="T").order_by("create_date")[:12]
    top_student_class = Class.objects.filter(enable="T").annotate(num_students=Count('students_in_class')).order_by("-num_students")[:13]
    if request.method == 'POST':
        if request.is_ajax():
            search_word = request.POST['search_word']
            all_class = Class.objects.filter(Q(enable="T"), Q(class_name__icontains=search_word) | Q(teacher__username__icontains=search_word))
            teacher = []
            for each_class in all_class:
                teacher.append(each_class.teacher)
            print teacher
            all_class = serializers.serialize('json', all_class )
            all_class = simplejson.loads( all_class )

            teacher = serializers.serialize('json', teacher )
            teacher = simplejson.loads( teacher )

            data = simplejson.dumps( {'all_class':all_class, 'teacher':teacher} )
            return HttpResponse( data, mimetype='application/json' )
        if "login" in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth_login(request, user)
                    recently_class = Class.objects.order_by("create_date")[:12]
                    top_student_class = Class.objects.annotate(num_students=Count('students_in_class')).order_by("-num_students")[:14]
                    return render(request, "home/home.html", {'all_class':all_class, 'recently_class':recently_class, 'top_student_class':top_student_class})
                else:
                    error = 'Your account has been disabled. We apologize for any inconvenience! If this is a mistake please contact our <a href="mailto:%s">support</a>.' % settings.SUPPORT_EMAIL
            else:
                error = '''Username and password didn't matched, if you forgot your password?'''
            return render(request, "home/home.html", {'all_class':all_class, 'recently_class':recently_class, 'top_student_class':top_student_class,'error': error })

    

    return render(request, "home/home.html", {'all_class':all_class, 'recently_class':recently_class, 'top_student_class':top_student_class })
 
def profile(request):
    user = request.user
    success = False
    if request.method == 'POST':
        upform = EditProfileForm(request.POST, instance=user.get_profile())
        upuserform= EditUserForm(request.POST,instance=user)
        if upform.is_valid() and upuserform.is_valid():
            user = upuserform.save()
            up = upform.save(commit=False)
            up.user = request.user
            if  upuserform.cleaned_data['password'] != "":
                user = User.objects.get(pk=request.user.pk)
                user.set_password(upuserform.cleaned_data['password'])
                user.save()
            if 'user_image' in request.FILES:
                up.user_image = request.FILES['user_image']
            up.save()
            success = True    
    else:
        upform = EditProfileForm(instance=user.get_profile())
        upuserform= EditUserForm(instance=user)
    return render(request,'home/profile.html',{
        'user':user,
        'upuserform':upuserform,
        'upform':upform,
        'success':success
        })
def about(request):
    return render(request, 'home/about.html');
    
