import os
import json
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q
from pywebpush import webpush, WebPushException # push notifications
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static

# Account Management

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
        else:
            return redirect("register")

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def profile(request):
    context = {
        'posts':Post.objects.filter(created_by=request.user).order_by('-id')
    }
    return render(request, 'users/profile.html', context)

@login_required
def get_friendship_with_user(request, this_user_id):
    friendship_to_find = Friendship.objects.filter(
        Q(from_user_id=request.user.id, to_user_id=this_user_id) |
        Q(to_user_id=request.user.id, from_user_id=this_user_id)
    ).first()
    return friendship_to_find

@login_required
def user_profile(request, username):
    this_user = User.objects.get(username=username)
    if this_user==request.user:
        return redirect(profile)
    friendship = get_friendship_with_user(request, this_user.id)
    # is_friend=False
    # if (friendship and friendship.is_active==True):
    #     is_friend=True
    users_post = Post.objects.filter(created_by=this_user).order_by('-id')
    context = {
        'friendship': friendship,
        # 'is_friend': is_friend,
        # 'is_friendship_active': friendship.is_active,
        'this_user': this_user,
        'posts': users_post,
    }
    return render(request, 'user_profile.html', context)

# index and posts

@login_required
def index(request):
    posts=Post.objects.order_by('-id')[:50]
    context = {
        'posts': posts,
        'posts_amount': len(posts),
    }
    return render(request, "index.html", context)

# post management

@login_required
def new_post(request):
    post_content = request.POST.get("post_content", "")
    this_post = Post.objects.create(content=post_content, created_by=request.user)
    context = {
        'this_post': this_post,
        'is_mine': True,
    }
    return render(request, "post_detail.html", context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    context = {
        'message': 'The post and all related comments were successfully erased',
    }
    return render(request, "message.html", context)

@login_required
def post_detail(request, post_id):
    this_post = get_object_or_404(Post, id=post_id)
    is_mine = False
    if request.user == this_post.created_by:
        is_mine = True
    comments = Comment.objects.filter(post=this_post).order_by('id')
    context = {
        'this_post': this_post,
        'is_mine': is_mine,
        'comments': comments,
    }
    return render(request, "post_detail.html", context)

# comment management

@login_required
def new_comment(request):
    comment_content = request.POST.get("comment_content", "")
    post_id = request.POST.get("post_id", "")
    post = get_object_or_404(Post, id=post_id)
    if post.created_by == request.user:
        Comment.objects.create(post=post, content=comment_content, created_by=request.user, seen=True)
    else:
        Comment.objects.create(post=post, content=comment_content, created_by=request.user, seen=False)
    return redirect(post_detail, post_id)

@login_required
def delete_comment(request):
    comment_id = request.POST.get("comment_id", "")
    comment_to_erase = get_object_or_404(Comment, id=comment_id)
    if comment_to_erase.created_by == request.user:
        comment_to_erase.delete()
        context = {
            'message': 'Your comment was successfully removed'
        }
        return render(request, 'message.html', context)
    else:
        context = {
            'message': 'You do not have the right\'s to remove another user\'s comment'
        }
        return render(request, 'message.html', context)

# search engine

@login_required
def search_results(request):
    search_text = request.POST.get("search_text", "")
    found_users = User.objects.filter(username__icontains=search_text)
    posts = Post.objects.filter(content__icontains=search_text)
    context = {
        'search_text': search_text,
        'found_users': found_users,
        'posts': posts
    }
    return render(request, "search_results.html", context)

@login_required
def conversation_search_results(request):
    search_text = request.POST.get("search_text", "")
    conversations = Conversation.objects.filter(
        Q(conversation_name__icontains=search_text) |
        Q(participants__username__icontains=search_text)
    ).filter(
        participants=request.user
    ).distinct()
    context = {
        'search_text': search_text,
        'conversations': conversations,
    }
    return render(request, "conversation_search_results.html", context)
# user interface

@login_required
def message(request, message):
    context = {
        'message': message,
    }
    return render(request, "message.html", context)

# friendship management

@login_required
def send_friendship_request(request, to_user_id):
    friendship = Friendship(from_user_id=to_user_id, to_user_id=request.user.id)
    if (friendship.DoesNotExist()):
        Friendship.objects.create(from_user_id=request.user.id, to_user_id=to_user_id)
        context = {
            'message': 'your friendship request was sent'
        }
    else:
        context = {
            'message': 'the user already requested you a friendship, find it in your Notifications'
        }
    return render(request, 'message.html', context)

@login_required
def block_user(request, user_to_block_id):
    friendship_to_deactivate = get_friendship_with_user(request, user_to_block_id)
    if friendship_to_deactivate:
        friendship_to_deactivate.is_active=False
        friendship_to_deactivate.save()
        context = {
            'message': 'User blocked'
        }
    else:
        context = {
            'message': 'could not block the user. Please try again'
        }
    return render(request, "message.html", context)

@login_required
def delete_friendship(request, to_user_id):
    friendship_to_remove = get_friendship_with_user(request, to_user_id)
    friendship_to_remove.delete()
    context = {
        'message': 'friendship removed'
    }
    return render(request, "message.html", context)

@login_required
def accept_friendship_request(request, friendship_request_id):
    friendship_request=get_object_or_404(Friendship, id=friendship_request_id)
    if friendship_request.is_active==False and friendship_request.to_user_id==request.user.id:
        friendship_request.is_active=True
        friendship_request.save()
        context = {
            'message': 'friendship request accepted'
        }
    else:
        context = {
            'message': 'there was an error while accepting the request'
        }
    return render(request, "message.html", context)

@login_required
def all_users(request):
    all_users = User.objects.all()
    context = {
        'all_users': all_users
    }
    return render(request, 'all_users.html', context)

@login_required
def remove_friendship_request(request, friendship_request_id):
    Friendship.objects.delete(id=friendship_request_id)
    context = {
        'message': 'your request was deleted'
    }
    return render(request, 'message.html', context)

@login_required
def get_comments_on_my_posts(request):
    received_comments = Comment.objects.filter(
        ~Q(created_by=request.user),
        post__created_by=request.user
    ).order_by('-id')
    return received_comments

@login_required
def get_my_friendship_requests(request):
    friendship_requests = Friendship.objects.filter(
        is_active=False,
        to_user_id=request.user.id,
    ).order_by('-id')
    return friendship_requests

# @login_required
# def visualize_notifications(received_comments, friendship_requests):
#     for friendship in friendship_requests:
#         if friendship.seen == False:
#             friendship.seen=True
#             friendship.save()
#     for comment in received_comments:
#         if comment.seen == False:
#             comment.seen=True
#             comment.save()
#     return

@login_required
def get_user_by_id(user_id):
    user = User.objects.get(id=user_id)
    return user

@login_required
def notifications(request):
    friendship_requests = Friendship.objects.filter(
        is_active=False,
        to_user_id=request.user.id,  # Assuming this is the field for the recipient
    )
    requests_with_usernames = []
    for request_obj in friendship_requests:
        from_user = User.objects.get(id=request_obj.from_user_id)  # Assuming from_user_id is the correct field
        requests_with_usernames.append({
            'id': request_obj.id,
            'from_user_id': request_obj.from_user_id,
            'from_user_username': from_user.username
        })
    received_comments = get_comments_on_my_posts(request)
    # visualize_notifications(received_comments, friendship_requests)
    for friendship in friendship_requests:
        if friendship.seen == False:
            friendship.seen = True
            friendship.save()
    for comment in received_comments:
        if comment.seen == False:
            comment.seen = True
            comment.save()
    context = {
        'requests_with_usernames': requests_with_usernames,
        'received_comments': received_comments,
    }
    return render(request, 'notifications.html', context)

@login_required
def save_push_subscription(request):
    if request.method == 'POST':
        try:
            subscription_data = json.loads(request.body)
            subscription, created = PushSubscription.objects.get_or_create(
                user=request.user,
                endpoint=subscription_data['endpoint'],
                defaults={
                    'p256dh': subscription_data['keys']['p256dh'],
                    'auth': subscription_data['keys']['auth']
                }
            )
            if created:
                print('LOG: Subscription created')
            else:
                print('LOG: Subscription already exists, updating')
                subscription.p256dh = subscription_data['keys']['p256dh']
                subscription.auth = subscription_data['keys']['auth']
                subscription.save()
            return JsonResponse({'status': 'Subscription saved successfully'})
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except KeyError as e:
            print(f"Missing key in subscription data: {str(e)}")
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            print(f"Error saving subscription: {str(e)}")
            return JsonResponse({'error': 'Failed to save subscription'}, status=400)
    else:
        print('LOG: Invalid request method')
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def my_conversations(request):
    conversations = Conversation.objects.filter(participants=request.user)
    context = {
        'conversations': conversations
    }
    return render(request, 'conversations.html', context)

@login_required
def conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by('id')[:50]
    for message in messages:
        if message.seen == False:
            message.seen = True
            message.save()
    context = {
        'conversation': conversation,
        'messages': messages,
    }
    return render(request, 'conversation.html', context)

@login_required
def chat_settings(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by('id')
    context = {
        'conversation': conversation,
        'messages': messages,
    }
    return render(request, 'chat_settings.html', context)

@login_required
def add_participants(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user.id == conversation.admin_id and request.method == "POST":
        friend_ids = request.POST.getlist('friends')  # Get list of selected friends
        for friend_id in friend_ids:
            friend = get_object_or_404(User, id=friend_id)
            conversation.participants.add(friend)  # Add each friend to the conversation
        return redirect('conversation', conversation_id=conversation_id)  # Redirect back to conversation view

@login_required
def remove_participants(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user.id == conversation.admin_id and request.method == "POST":
        participant_ids = request.POST.getlist('participants')  # Get list of participants to remove
        for participant_id in participant_ids:
            participant = get_object_or_404(User, id=participant_id)
            conversation.participants.remove(participant)  # Remove each participant
        return redirect('conversation', conversation_id=conversation_id)  # Redirect back to conversation view

@login_required
def new_conversation(request):
    conversation_name = request.POST.get("conversation_name", "")
    new_conversation = Conversation.objects.create(
        admin_id = request.user.id,
        conversation_name = conversation_name,
    )
    new_conversation.participants.add(request.user)
    context = {
        'conversation': new_conversation
    }
    return render(request, 'conversation.html', context)

@login_required
def delete_conversation(request):
    conversation_id = request.POST.get("conversation_id", "")
    conversation_to_delete = get_object_or_404(Conversation, id=conversation_id)
    conversation_to_delete.delete()
    context = {
        'message': 'The conversation and all it\'s contents were successfully erased'
    }
    return render(request, 'message.html', context)

@login_required
def leave_conversation(request):
    conversation_id = request.POST.get("conversation_id", "")
    conversation_to_leave = get_object_or_404(Conversation, id=conversation_id)
    Message.objects.create(sender=request.user, conversation=conversation_to_leave, content='** leaving the conversation... **')
    conversation_to_leave.participants.remove(request.user)
    context = {
        'message': 'You left the conversation'
    }
    return render(request, 'message.html', context)

@login_required
def new_message(request, conversation_id):
    message_text = request.POST.get("message_text", "")
    destination_conversation = get_object_or_404(Conversation, id=conversation_id)
    Message.objects.create(sender=request.user, conversation=destination_conversation, content=message_text)
    # # PUSH NOTIFICATIONS
    # subscriptions = PushSubscription.objects.filter(user_id__in=destination_conversation.participants.exclude(id=request.user.id).values_list('id', flat=True))
    # payload = json.dumps({
    #     'title': 'New message on Algrant',
    #     'body': f"{request.user.username}: {message_text}",
    #     'icon': '{% url static  %}'  # Personalizza l'icona se necessario
    # })
    # for subscription in subscriptions:
    #     subscription_info = {
    #         'endpoint': subscription.endpoint,
    #         'keys': {
    #             'p256dh': subscription.p256dh,
    #             'auth': subscription.auth
    #         }
    #     }
    #     send_push_notification(subscription_info, payload)
    # Send push notifications to participants
    participants = destination_conversation.participants.exclude(id=request.user.id)
    subscriptions = PushSubscription.objects.filter(user__in=participants)
    for subscription in subscriptions:
        send_push_notification(subscription, message_text)
    return redirect(conversation, conversation_id)
    # return JsonResponse({"status": "message created"})

@login_required
def delete_message(request):
    message_id = request.POST.get("message_id", "")
    conversation_id = request.POST.get("conversation_id", "")
    message_to_delete = get_object_or_404(Message, id=message_id)
    if request.user == message_to_delete.sender:
        message_to_delete.content = '** message deleted **'
        message_to_delete.save()
        return redirect(conversation, conversation_id)
    else:
        context = {
            'message': 'You don\'t have the rights to erase the selected message'
        }
        return render(request, 'message.html', context)

def send_push_notification(subscription, message_content):
    try:
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": {
                    "p256dh": subscription.p256dh,
                    "auth": subscription.auth,
                }
            },
            data=json.dumps({
                "title": "New message",
                "body": message_content,
                "icon": static('icons/PulsarBlackBorder.png')
            }),
            vapid_private_key=os.getenv('VAPID_PRIVATE_KEY'),
            vapid_claims={
                "sub": "mailto:sebastianimarco@proton.me"
            }
        )
        print("Push notification sent successfully!")
    except WebPushException as ex:
        print("Failed to send push notification: {}", repr(ex))