from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from study import views
from class_management import *
from study import views
from study.views import *
urlpatterns = patterns('',
    url(r'^study/$', views.study, name='study'),
    url(r'^(?P<pk>\d+)/studyclass/$', views.studyclass, name='studyclass'),
    url(r'^(?P<class_id>\d+)/studyclass/(?P<pke>\d+)/lesson/$', views.lesson, name='lesson'),
    url(r'^(?P<class_id>\d+)/studyclass/(?P<lesson_id>\d+)/lesson/(?P<pk>\d+)/test/$', views.test, name='test'),
    url(r'^(?P<class_id>\d+)/studyclass/(?P<lesson_id>\d+)/lesson/(?P<test_id>\d+)/result/$', views.result, name='result'),
    url(r'^question/(?P<test_id>\d+)/$', views.question, name="question"),
    url(r'^leave_class/(?P<class_id>\d+)/$', views.leave_class, name="leaveclass"),
    url(r'^questionback/(?P<test_id>\d+)/$', views.questionback, name="questionback")
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)