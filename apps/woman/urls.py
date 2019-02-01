from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^join$', views.join),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^groups$', views.main_groups),
    url(r'^add_group$', views.add_groups),
    url(r'^user/(?P<id>\d+)$', views.users),
    url(r'^group/edit_group/(?P<id>\d+)$', views.edit_group),
    url(r'^group/edit_post/(?P<id>\d+)$', views.edit_post),
    url(r'^group/user/(?P<id>\d+)$', views.group_users),
    url(r'^group/(?P<id>\d+)$', views.groups),
    url(r'^group_likes/(?P<id>\d+)$', views.group_likes),
    url(r'^post_likes/(?P<id>\d+)$', views.post_likes),
    url(r'^logout$', views.logout),
    url(r'^comment/(?P<id>\d+)$', views.comment),
    url(r'^group/delete_post/(?P<id>\d+)$', views.delete_post),
    url(r'^group/delete_comment/(?P<id>\d+)$', views.delete_comment),
    url(r'^group/(?P<id>\d+)/add_post$', views.add_post),
]