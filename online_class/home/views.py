from django.shortcuts import *
from home.forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.

def register(request):
    # context=RequestContext(request)
    registered=False

    if request.method =='POST':
        user_form=UserForm(data=request.POST) 
        profile_form=UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        else:
            print user_form.errors, profile_form.errors
    else:
        user_form=UserForm()
        profile_form=UserProfileForm()
    
    return render(request,
            'home/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def home(request):
    return render(request,'home/home.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print user
        if user:
            if user.is_active:
                auth_login(request, user)
                return render(request, "home/home.html")
            else:
                error = 'Your account has been disabled. We apologize for any inconvenience! If this is a mistake please contact our <a href="mailto:%s">support</a>.' % settings.SUPPORT_EMAIL
        else:
            error = '''Username and password didn't matched, if you forgot your password?'''
        return render(request, "home/login.html", {'error': error })
    return render(request, "home/login.html")

# @login_required
# def restricted(request):
#     return render(request,'Please login!!')
@login_required
def logout(request):
    auth_logout(request)
    return render(request,'home/home.html') 

def alone(request):
    return render(request,'home/alone.html')