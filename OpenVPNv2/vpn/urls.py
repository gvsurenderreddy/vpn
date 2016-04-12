from django.conf.urls import patterns, include, url

import vpn.views
urlpatterns = [
     url(r'^home/', vpn.views.status_vpn, name='status_vpn'),
     url(r'^manage/vpn/(?P<vpn_id>\d+)', vpn.views.managment_vpn),
     url(r'^manage/addcomment/(?P<vpn_id>\d+)/$', vpn.views.addcomment),
     url(r'^contact/$', vpn.views.contact),
     url(r'^cert/$', vpn.views.create_cert_usr, name="cert"),
     url(r'^revoke/$', vpn.views.revoke_cert_usr, name="revoke"),
     url(r'^status/$', vpn.views.status_cert, name="status"),
     url(r'^drop/$', vpn.views.dropdown),
     url(r'^index/$', vpn.views.home_page1),
     url(r'^list_vpn/$', vpn.views.list_vpn, name="list_vpn" ),
     url(r'^manage_cert/vpn/(?P<vpn_id>\d+)', vpn.views.tabs, name="tabs"),
     url(r'^c/$', vpn.views.home_page2, name="home_page2"),
]

