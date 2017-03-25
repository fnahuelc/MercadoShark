from django.conf.urls import url
from . import views

app_name = 'managerApp'
urlpatterns = [
    # /managerApp/
    url(r'^$', views.index, name='index'),

    # /manaerApp/ #_article_Number/
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),

    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^create_article/$', views.create_article, name='create_article'),
    url(r'^(?P<article_id>[0-9]+)/delete_article/$', views.delete_article, name='delete_article'),

]

