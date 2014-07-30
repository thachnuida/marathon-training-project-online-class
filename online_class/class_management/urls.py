from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from class_management import views
from class_management.views import *

urlpatterns = patterns('',
    url(r'^$', classlist, name='classlist'),
    url(r'^create-class/$', create_class, name='createclass'),
    url(r'^(?P<pk>\d+)/detail-class/$', detail_class, name='detailclass'),
    url(r'^(?P<pk>\d+)/student-class/$', studentclass, name='studentclass'),
    url(r'^(?P<class_id>\d+)/create-lesson/$', create_lesson, name='createlesson'),
    url(r'^(?P<class_id>\d+)/lesson/(?P<pk>\d+)/$', detail_lesson, name='detaillesson'),
    url(r'^(?P<class_id>\d+)/lesson/(?P<lesson_id>\d+)/create-test/(?P<test_id>\d+)/$', create_test, name='createtest'),
    url(r'^(?P<class_id>\d+)/lesson/(?P<lesson_id>\d+)/detail-test/(?P<test_id>\d+)/$', detail_test, name='detailtest'),
    url(r'^test/(?P<test_id>\d+)/update-question/$', update_question, name="updatequestion"),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
