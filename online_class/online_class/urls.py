from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'online_class.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^class/', include('class_management.urls', namespace='classes')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^home/', include('home.urls', namespace='home')),
    url(r'^study/', include('study.urls', namespace='study')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

