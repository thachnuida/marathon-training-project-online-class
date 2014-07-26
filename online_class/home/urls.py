from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^alone/$',views.alone,name='alone')
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)