"""
URL configuration for algrant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from algrantapp.views import register, profile
# static files
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', include('algrantapp.urls')),
    # USER MANAGEMENT
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("accounts/profile/", profile, name="profile"),
    # admin
    path('admin/', admin.site.urls),
    # serve  static files and javascript files
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
