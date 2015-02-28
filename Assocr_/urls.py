from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from assocr import views

urlpatterns = patterns('',
    url(r'^assocr/', include('assocr.urls')),
    url(r'^assocr/accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',(r'^media/(?P<path>.*)','serve',{'document_root': settings.MEDIA_ROOT}), )