from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def default(request):
	return HttpResponseRedirect(reverse('home:home'))