from django.conf.urls import url
from . import views

app_name = 'managerApp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_article/$', views.create_article, name='create_article'),
    url(r'^create_testUser/$', views.create_testUser, name='create_testUser'),
    url(r'^login_mlUser/$', views.login_mlUser, name='login_mlUser'),
    url(r'^show_response/$', views.show_response, name='show_response'),
    url(r'^select_account/(?P<account_id>[0-9]+)$', views.select_account, name='select_account'),
    url(r'^(?P<article_id>[0-9]+)/delete_articles/$', views.delete_article, name='delete_articles'),
    url(r'^delete_account/(?P<account_id>[0-9]+)/$', views.delete_account, name='delete_account'),
    url(r'^prueba$', views.get_access_token, name='prueba'),
    url(r'^get_access_token$', views.get_access_token, name='get_access_token'),
    url(r'^get_access_token/(?P<code>w{0,150})$', views.get_access_token, name='getting_access_token')
]

