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
            # profile.user_image=profile_form.cleaned_data['user_image'],
            if 'user_image' in request.FILES:
                profile.user_image = request.FILES['user_image']
            profile.save()
            registered = True
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user.is_active:
                auth_login(request, user)
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
    return render(request,
            'home/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print user
        if user:
            if user.is_active:
                auth_login(request, user)
                currentuser = UserProfile.objects.get(user=request.user.id)
                return render(request, "home/home.html", {'currentuser':currentuser})
            else:
                error = 'Your account has been disabled. We apologize for any inconvenience! If this is a mistake please contact our <a href="mailto:%s">support</a>.' % settings.SUPPORT_EMAIL
        else:
            error = '''Username and password didn't matched, if you forgot your password?'''
        return render(request, "home/home.html", {'error': error })
    if request.user.is_anonymous():
        return render(request, "home/home.html")
    else :
        currentuser = UserProfile.objects.get(user=request.user.id)
        return render(request, "home/home.html", {'currentuser':currentuser})

def home(request):
    all_class = Class.objects.all()
    true=True
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                currentuser = UserProfile.objects.get(user=request.user.id)
                # all_class=all_class.exclude(students_in_class=request.user)
                paginator = Paginator(all_class, 8) # Show 8 contacts per page
                page = request.GET.get('page')
                try:
                    all_class = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    all_class = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    all_class = paginator.page(paginator.num_pages)
                recently_class = Class.objects.exclude(students_in_class=request.user).order_by("create_date")[:12]
                top_student_class = Class.objects.exclude(students_in_class=request.user).annotate(num_students=Count('students_in_class')).order_by("-num_students")[:14]
                return render(request, "home/home.html", {'currentuser':currentuser, 'all_class':all_class, 'recently_class':recently_class, 'top_student_class':top_student_class})
            else:
                error = 'Your account has been disabled. We apologize for any inconvenience! If this is a mistake please contact our <a href="mailto:%s">support</a>.' % settings.SUPPORT_EMAIL
        else:
            error = '''Username and password didn't matched, if you forgot your password?'''
        return render(request, "home/home.html", {'error': error })
    if request.user.is_anonymous():
        recently_class = Class.objects.order_by("create_date")[:12]
        paginator = Paginator(all_class, 8) # Show 8 contacts per page
        page = request.GET.get('page')
        try:
            all_class = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_class = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            all_class = paginator.page(paginator.num_pages)
        top_student_class = Class.objects.annotate(num_students=Count('students_in_class')).order_by("-num_students")[:13]
        return render(request, "home/home.html", {'all_class': all_class, 'recently_class':recently_class, 'top_student_class':top_student_class})
    else :
        recently_class = Class.objects.exclude(students_in_class=request.user).order_by("create_date")[:12]
        all_class=all_class.exclude(students_in_class=request.user)
        currentuser = UserProfile.objects.get(user=request.user.id)
        paginator = Paginator(all_class, 8) # Show 8 contacts per page
        page = request.GET.get('page')
        try:
            all_class = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_class = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            all_class = paginator.page(paginator.num_pages)
        top_student_class = Class.objects.exclude(students_in_class=request.user).annotate(num_students=Count('students_in_class')).order_by("-num_students")[:13]
        return render(request, "home/home.html", {'currentuser':currentuser, 'all_class':all_class, 'recently_class':recently_class, 'top_student_class':top_student_class})
 
def profile(request):
    user_using=request.user
    currentuser = UserProfile.objects.get(user=request.user.id)
    profiles = UserProfile.objects.filter(user=user_using)
    profiles2  =User.objects.filter(pk=user_using.id)
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        upform = EditProfileForm(request.POST, instance=user.get_profile())
        upuserform= EditUserForm(request.POST,instance=user_using)
        if upform.is_valid() and upuserform.is_valid():
            user = upuserform.save()
            up = upform.save(commit=False)
            up.user = request.user
            # profile.user_image=profile_form.cleaned_data['user_image'],
            if 'user_image' in request.FILES:
                up.user_image = request.FILES['user_image']
            up.save()    
    else:
        upform = EditProfileForm(instance=user.get_profile())
        upuserform= EditUserForm(instance=user_using)
    return render(request,'home/profile.html',{
        'profiles':profiles,
        'profiles2':profiles2,
        'upuserform':upuserform,
        'upform':upform,
        'currentuser':currentuser
        })