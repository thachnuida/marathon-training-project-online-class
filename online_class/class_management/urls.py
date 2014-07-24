from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from class_management import views
from class_management.views import *

urlpatterns = patterns('',
	# method 1
    # url(r'^$', views.index, name='index'),
    # # ex: /polls/5/
    url(r'^(?P<teacher_id>\d+)/$', views.classlist, name='classlist'),
    url(r'^create-class/$', create_class, name='createclass'),
    # # ex: /polls/5/results/
    # url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^search/$', views.search, name='search'),
    # url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
