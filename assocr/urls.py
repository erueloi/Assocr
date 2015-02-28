# from django.conf import settings
from django.conf.urls import patterns, url
from assocr import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^association/(?P<association_id>[\w\-]+)/$', views.association, name='association'),
        url(r'^add_association/$', views.add_association, name='add_association'),
        url(r'^association/(?P<association_id>[\w\-]+)/add_uf/$', views.add_uf, name='add_uf'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/$', views.uf, name='uf'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/add_member/$', views.add_member, name='add_member'),
        )