from django.conf.urls import patterns, include, url
from django.contrib import admin
from assocr import views

urlpatterns = patterns('',
    url(r'^assocr/', include('assocr.urls')),
    url(r'^assocr/accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
