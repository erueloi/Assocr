# from django.conf import settings
from django.conf.urls import patterns, url
from assocr import views
from django.contrib.auth.decorators import login_required
from assocr.views import MembersExport, MemberImport, MemberProcessImport

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_association/$', views.add_association, name='add_association'),
        url(r'^association/(?P<association_id>[\w\-]+)/$', views.association, name='association'),
        url(r'^association/(?P<association_id>[\w\-]+)/edit/$', views.add_association, name='edit_association'),
        url(r'^association/(?P<association_id>[\w\-]+)/add_uf/$', views.add_uf, name='add_uf'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/$', views.uf, name='uf'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/edit/$', views.add_uf, name='edit_uf'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/add_member/$', views.add_member, name='add_member'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/member/(?P<member_id>[\w\-]+)/$', views.member, name='member'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/member/(?P<member_id>[\w\-]+)/edit/$', views.add_member, name='edit_member'),
        url(r'^association/(?P<association_id>[\w\-]+)/export/$', login_required(MembersExport.as_view()), name='members_export'),
        )

#export - import
urlpatterns += patterns('',
        url(r'^association/(?P<association_id>[\w\-]+)/export/$', login_required(MembersExport.as_view()), name='members_export'),
        url(r'^association/(?P<association_id>[\w\-]+)/import/$', login_required(MemberImport.as_view()), name='members_import'),
        url(r'^association/(?P<association_id>[\w\-]+)/process_import/$',     login_required(MemberProcessImport.as_view()), name='members_process_import'),
        )

#handler404 = views.page_not_found
