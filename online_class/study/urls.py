from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from study import views
from class_management import *
from study import views
from study.views import *
urlpatterns = patterns('',
    url(r'^study/$', views.study, name='study'),
    url(r'^join/$', views.join, name='join'),
    url(r'^(?P<pk>\d+)/studyclass/$', views.studyclass, name='studyclass'),
    url(r'^(?P<pk>\d+)/joinclass/$', views.joinclass, name='joinclass'),
    url(r'^(?P<class_id>\d+)/studyclass/(?P<pke>\d+)/lesson/$', views.lesson, name='lesson'),
    url(r'^(?P<class_id>\d+)/studyclass/(?P<lesson_id>\d+)/lesson/(?P<pk>\d+)/test/$', views.test, name='test'),
    # url(r'^register/$',views.register,name='register'),
    # url(r'^logout/$',views.logout,name='logout'),
    # # url(r'^login/$',views.login,name='login'),
    # url(r'^alone/$',views.alone,name='alone'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)