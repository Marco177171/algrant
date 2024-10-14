from django.db.models import Q
from django.contrib.auth.models import User
from .models import Comment, Friendship

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
                'unseen_comments': unseen_comments
            }
    else:
        return {
            'unseen_friendship_requests': [],
            'unseen_comments': []
        }