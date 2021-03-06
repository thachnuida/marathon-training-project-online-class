from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$','django.contrib.auth.views.logout',{'next_page': '/home'},name='logout'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^about/$',views.about,name='about'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)