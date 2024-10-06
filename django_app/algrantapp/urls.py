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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('register', views.register, name='register'),
    path('new_post', views.new_post, name='new_post'),
    # path('delete_post', views.delete_post, name='delete_post'),
    path('post_detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('new_comment/<int:post_id>', views.new_comment, name='new_comment'),
    path('search_results', views.search_results, name='search_results')
]
