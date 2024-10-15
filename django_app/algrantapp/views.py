from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q

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
        'post': this_post,
    }
    return render(request, "post_detail.html", context)

@login_required
def delete_post(request, post_id):
    Post.objects.delete(id=post_id)
    context = {
        'message': 'The post and all related comments were successfully erased',
    }
    return redirect("message.html", context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-id')
    context = {
        'post': post,
        'comments': comments
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
#         if friendship.seen_by_to_user == False:
#             friendship.seen_by_to_user=True
#             friendship.save()
#     for comment in received_comments:
#         if comment.seen_by_to_user == False:
#             comment.seen_by_to_user=True
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
def my_conversations(request):
    conversations = Conversation.objects.filter(participants=request.user)
    context = {
        'conversations': conversations
    }
    return render(request, 'conversations.html', context)

@login_required
def conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by('id')
    context = {
        'conversation': conversation,
        'messages': messages,
    }
    return render(request, 'conversation.html', context)

@login_required
def new_message(request, conversation_id):
    message_text = request.POST.get("message_text", "")
    destination_conversation = get_object_or_404(Conversation, id=conversation_id)
    Message.objects.create(sender=request.user, conversation=destination_conversation, content=message_text)
    return redirect(conversation, conversation_id)