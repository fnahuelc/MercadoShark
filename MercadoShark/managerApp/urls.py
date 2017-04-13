from django.conf.urls import url
from . import views

app_name = 'managerApp'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^create_item/$', views.create_item, name='create_item'),
    url(r'^(?P<item_id>[0-9]+)/delete_items/$', views.delete_items, name='delete_items'),

    url(r'^create_testUser/$', views.create_testUser, name='create_testUser'),
    url(r'^login_mlUser/$', views.login_mlUser, name='login_mlUser'),
    url(r'^delete_account/(?P<account_id>[0-9]+)/$', views.delete_account, name='delete_account'),
    url(r'^select_account/(?P<account_id>[0-9]+)$', views.select_account, name='select_account'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^get_access_token$', views.get_access_token, name='get_access_token'),

    url(r'^authorize_meli$', views.authorize_meli, name='authorize_meli'),
    url(r'^authorize_meli/(?P<code>w{0,150})$', views.authorize_meli, name='authorizing_meli')

]

