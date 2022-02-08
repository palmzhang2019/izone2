# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import profile_view, change_profile_view, github_auth, githhub_login


urlpatterns = [
    url(r'^profile/$', profile_view, name='profile'),
    url(r'^profile/change/$', change_profile_view, name='change_profile'),
    url(r'github/$', github_auth, name='github_oauth'),
    url(r'github_login/$', githhub_login, name='github_login'),
]