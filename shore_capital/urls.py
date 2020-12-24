"""shore_capital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from file import views
import os

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('login.urls'), name='login'),
	path('user', include('user.urls'), name='user'),
	path('file', include('file.urls'), name='file'),
    path('superadmin', include('superadmin.urls'), name='superadmin'),
    path('company/', include('company.urls'), name='company'),
    path('role/', include('role.urls'), name='role'),
    path('group/', include('group.urls'), name='group'),
    path('fp/', include('django_drf_filepond.urls'), name='filepond_upload'),
    path('password/', include('password.urls'), name='password'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
