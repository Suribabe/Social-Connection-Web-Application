"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
# from django.contrib.auth import views as auth_views
# from django.contrib import admin
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# import django.contrib.auth.views
import django.contrib.auth.views
import grumblr.views
from django.conf import settings
import os
from django.conf.urls.static import static

from django.views.static import serve as staticserve
urlpatterns = [
    
    # url(r'^grumblr/', include('grumblr.urls')),
    url(r'^$', grumblr.views.home),
    url(r'^grumblr/main', grumblr.views.home),
    url(r'^create-user', grumblr.views.create_user),
    url(r'^create-post/(?P<last_post>\d+)$',grumblr.views.create_post,name="post"),
    url(r'^create-comment/(?P<post_id>\d+)$',grumblr.views.create_comment),
    url(r'^follow/(?P<id>\d+)$',grumblr.views.follow),
    url(r'^unfollow/(?P<id>\d+)$',grumblr.views.unfollow),
    url(r'^profile/(?P<profileid>\d+)$', grumblr.views.getProfile),
    url(r'^photo/(?P<id>\d+)$',grumblr.views.getPhoto, name='photo'),
    url(r'^update/', grumblr.views.update),
    url(r'^confirm/(?P<username>.*)/(?P<token>.*)$',
        grumblr.views.confirm_registration, name='confirm'),
    url(r'^get-update/(?P<last_post>\d+)$',grumblr.views.get_update),
    # url(r'^password_change/done/$',grumblr.views.changePassword,name="my_password_change"),
    url(r'^changepassword/', grumblr.views.changePassword),
    url(r'^follows/', grumblr.views.getFollows),
    url(r'^logout$',django.contrib.auth.views.logout_then_login),
    url(r'^grumblr/login$', django.contrib.auth.views.login, {'template_name':'login.html'}, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, 'FORCE_SERVE_STATIC', False):
    settings.DEBUG = True
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    settings.DEBUG = False