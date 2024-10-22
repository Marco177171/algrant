from django.conf import settings
import os
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Comment, Conversation, Message, Friendship

def get_my_friends(request):
    if request.user.is_authenticated:
        friendships = Friendship.objects.filter((Q(from_user_id=request.user.id) | Q(to_user_id=request.user.id)) & Q(is_active=True))
        friend_id_list = []
        for friendship in friendships:
            if friendship.to_user_id != request.user.id:
                friend_id_list.append(friendship.to_user_id)
            else:
                friend_id_list.append(friendship.from_user_id)
        people = User.objects.filter(id__in=friend_id_list)
        return {
            'my_friends_list': people
        }
    else:
        return {
            'my_friends_list': []
        }

def notification_context(request):
    if request.user.is_authenticated:
        unseen_friendship_requests = Friendship.objects.filter(
                to_user_id=request.user.id,
                is_active=False,
                seen=False
            ).count()
        unseen_comments = Comment.objects.filter(
                post__created_by=request.user,
                seen=False
            ).count()
        return {
                'unseen_friendship_requests': unseen_friendship_requests,
                'unseen_comments': unseen_comments,
            }
    else:
        return {
            'unseen_friendship_requests': '0',
            'unseen_comments': '0',
        }
    
def conversations_context(request):
    if request.user.is_authenticated:
        conversations = Conversation.objects.filter(
            Q(participants=request.user)
        )
        unseen_messages = Message.objects.filter(
            conversation__in = conversations,
            seen = False,
        ).count()
        return {
                'unseen_messages': unseen_messages,
            }
    else:
        return {
            'unseen_messages': '0',
        }
    
def environ(request):
    return {
        'vapid_public_key': settings.VAPID_PUBLIC_KEY,
    }

# def read_vapid_public_key():
#     key_file = os.path.join(os.path.dirname(__file__), 'vapid_public_key.txt')
#     with open(key_file, 'r') as f:
#         vapid_key = f.read().strip()
#     return {'vapid_public_key': vapid_key}