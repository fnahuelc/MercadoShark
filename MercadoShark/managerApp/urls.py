from django.conf.urls import url
from . import views

app_name = 'managerApp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_item/$', views.create_item, name='create_item'),
    url(r'^closed_item/(?P<item_id>[0-9]+)/$', views.closed_item, name='closed_item'),
    url(r'^paused_item/(?P<item_id>[0-9]+)/$', views.paused_item, name='paused_item'),
    url(r'^active_item/(?P<item_id>[0-9]+)/$', views.active_item, name='active_item'),
    url(r'^delete_item/(?P<item_id>[0-9]+)/$', views.delete_item, name='delete_item'),
    url(r'^authorize_meli$', views.authorize_meli, name='authorize_meli'),
    url(r'^authorize_meli/(?P<code>w{0,150})$', views.authorize_meli, name='authorizing_meli'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

]

