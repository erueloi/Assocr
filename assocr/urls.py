# from django.conf import settings
from django.conf.urls import patterns, url
from assocr import views
from django.contrib.auth.decorators import login_required
from assocr.importexport import MembersExport, MemberImport, MemberProcessImport, GenerateXmlSEPAExport

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
        url(r'^calendar/(?P<association_id>[\w\-]+)/$', views.calendar, name='calendar'),
        url(r'^usert-to-association/$', views.user_to_association, name='user_to_association'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/add_receipt/$', views.add_receipt, name='add_receipt'),
        url(r'^association/(?P<association_id>[\w\-]+)/uf/(?P<uf_id>[\w\-]+)/receipt/(?P<receipt_id>[\w\-]+)/edit/$', views.add_receipt, name='edit_receipt'),
        )

#export - import
urlpatterns += patterns('',
        url(r'^association/(?P<association_id>[\w\-]+)/export/$', login_required(MembersExport.as_view()), name='members_export'),
        url(r'^association/(?P<association_id>[\w\-]+)/import/$', login_required(MemberImport.as_view()), name='members_import'),
        url(r'^association/(?P<association_id>[\w\-]+)/process_import/$',     login_required(MemberProcessImport.as_view()), name='members_process_import'),
        url(r'^association/(?P<association_id>[\w\-]+)/xml_sepa/$', login_required(GenerateXmlSEPAExport.as_view()), name='xml_sepa'),
        )

urlpatterns += patterns('',
        url(r'^get_association_user/(?P<user_id>[\w\-]+)/$', views.get_association_user, name='get_association_user'),
        url(r'^generate_receipts/(?P<association_id>[\w\-]+)/$', views.generate_receipts, name='generate_receipts'),
        url(r'^cancel_uf/(?P<uf_id>[\w\-]+)/$', views.cancel_uf, name='cancel_uf'),
        url(r'^active_uf/(?P<uf_id>[\w\-]+)/$', views.active_uf, name='active_uf'),
        )

#handler404 = views.page_not_found
