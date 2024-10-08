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
    # ACCOUNT MANAGEMENT
    path('profile', views.profile, name='profile'),
    path('user_profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('register', views.register, name='register'),
    path('user_logout', views.user_logout, name='user_logout'),
    # POSTING
    path('new_post', views.new_post, name='new_post'),
    path('post_detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('delete_post', views.delete_post, name='delete_post'),
    # COMMENTING
    path('new_comment', views.new_comment, name='new_comment'),
    path('search_results', views.search_results, name='search_results'),
    # FRIENDSHIP MANAGEMENT
    path('all_users', views.all_users, name='all_users'),
    path('send_friendship_request/<int:to_user_id>', views.send_friendship_request, name='send_friendship_request'),
    path('block_user/<int:user_to_block_id>', views.block_user, name='block_user'),
    path('delete_friendship/<int:to_user_id>', views.delete_friendship, name='delete_friendship'),
    path('accept_friendship_request/<int:friendship_request_id>', views.accept_friendship_request, name='accept_friendship_request'),
    # NOTIFICATIONS
    path('notifications', views.notifications, name='notifications'),
    # USER INTERFACE
    path('message', views.message, name='message'),
]
