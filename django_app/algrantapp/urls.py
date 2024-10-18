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
    path('user_profile/<str:username>', views.user_profile, name='user_profile'),
    path('register', views.register, name='register'),
    path('user_logout', views.user_logout, name='user_logout'),
    # POSTING
    path('new_post', views.new_post, name='new_post'),
    path('post_detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    # COMMENTING
    path('new_comment', views.new_comment, name='new_comment'),
    path('delete_comment', views.delete_comment, name='delete_comment'),
    # FRIENDSHIP MANAGEMENT
    path('all_users', views.all_users, name='all_users'),
    path('send_friendship_request/<int:to_user_id>', views.send_friendship_request, name='send_friendship_request'),
    path('block_user/<int:user_to_block_id>', views.block_user, name='block_user'),
    path('delete_friendship/<int:to_user_id>', views.delete_friendship, name='delete_friendship'),
    path('accept_friendship_request/<int:friendship_request_id>', views.accept_friendship_request, name='accept_friendship_request'),
    # CHATS
    path('my_conversations', views.my_conversations, name='my_conversations'),
    path('my_conversations/<str:conversation_id>', views.conversation, name='conversation'), # channels
    path('new_conversation', views.new_conversation, name='new_conversation'),
    path('delete_conversation', views.delete_conversation, name='delete_conversation'),
    # CHAT SETTINGS
    path('my_conversations/<str:conversation_id>/settings', views.chat_settings, name='chat_settings'),
    path('my_conversations/<int:conversation_id>/add', views.add_participants, name='add_participants'),
    path('my_conversations/<int:conversation_id>/remove', views.remove_participants, name='remove_participants'),
    path('leave_conversation', views.leave_conversation, name='leave_conversation'),
    # MESSAGES
    path('new_message/<int:conversation_id>', views.new_message, name='new_message'),
    path('delete_message', views.delete_message, name='delete_message'),
    # NOTIFICATIONS
    path('notifications', views.notifications, name='notifications'),
    # USER INTERFACE
    path('message', views.message, name='message'), # get a message when something happens
    path('search_results', views.search_results, name='search_results'),
]
