from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
def login(request):
    if request.method == 'POST':
    	username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('classes:classlist'))
                # return render(request, {{ url 'classlist' }})
            else:
                error = 'Your account has been disabled. We apologize for any inconvenience! If this is a mistake please contact our <a href="mailto:%s">support</a>.' % settings.SUPPORT_EMAIL
        else:
            error = '''Username and password didn't matched, if you forgot your password? <a href="%s">Request new one</a>''' % reverse('accounts_forgot_password')
        return render(request, "home/login.html", {'error': error })
    return render(request, "home/login.html")