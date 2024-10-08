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
    path('base', views.base, name='base'),
    # ACCOUNT MANAGEMENT
    path('profile', views.profile, name='profile'),
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('register', views.register, name='register'),
    # POSTING
    path('new_post', views.new_post, name='new_post'),
    path('post_detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('delete_post', views.delete_post, name='delete_post'),
    # COMMENTING
    path('new_comment', views.new_comment, name='new_comment'),
    path('search_results', views.search_results, name='search_results'),
    # FRIENDSHIP MANAGEMENT
    path('send_friendship_request', views.send_friendship_request, name='send_friendship_request'),
    # USER INTERFACE
    path('message', views.message, name='message'),
]
