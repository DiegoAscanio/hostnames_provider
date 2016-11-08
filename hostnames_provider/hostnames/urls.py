'''
        @file urls.py
        @lastmod 8/11/2016
'''

# Importacoes
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views

from views import HostDetail
from . import views
from . import models



# Area de criacao de urls
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajuda$', views.help, name='help'),
    url(r'^perfil$', views.profile, name='profile'),
    url(r'^opcoes$', views.options, name='options'),
    url(r'^rest/search__ip__address/(?P<ip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$', views.host_detail_ipaddress),
    url(r'^rest/search__mac__address/(?P<mac>[0-9a-f]{2}\:[0-9a-f]{2}\:[0-9a-f]{2}\:[0-9a-f]{2}\:[0-9a-f]{2}\:[0-9a-f]{2})$', views.host_detail_macaddress),
    url(r'^rest/list/$',views.HostList.as_view(), name='restlist'),
    url(r'^rest/detail/(?P<pk>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$',views.HostDetail.as_view(), name='restdetail'),
    url(r'^error/$', views.error, name='error'),
    url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name='admin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hostname/$', views.hostname, name='hostname'),
    url(r'^create/$', views.create, name='create'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^download/$', views.download, name='download'),
    url(r'^update/$', views.update, name='update'),
    url(r'^retrieve/$', views.retrieve, name='retrieve'),
    url(r'^list/$', views.list, name='list'),
    url(r'^pesquisar/$', views.pesquisar, name='pesquisar'),
    url(r'^delete/$', views.delete, name='delete'),
]
