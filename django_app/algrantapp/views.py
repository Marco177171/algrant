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
def user_password_change(request):
    password_change(request)
    return redirect("password_change")

@login_required
def profile(request):
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
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
def user_profile(request, user_id):
    this_user = get_object_or_404(User, id=user_id)
    if this_user==request.user:
        return redirect(profile)
    friendship = get_friendship_with_user(request, this_user.id)
    # is_friend=False
    # if (friendship and friendship.is_active==True):
    #     is_friend=True
    users_post = Post.objects.filter(created_by=this_user).order_by('-id')
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
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
    posts=Post.objects.order_by('-id')
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
        'posts': posts,
        'posts_amount': len(posts),
    }
    return render(request, "index.html", context)

# post management

@login_required
def new_post(request):
    post_content = request.POST.get("post_content", "")
    this_post = Post.objects.create(content=post_content, created_by=request.user)
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
        'post': this_post,
    }
    return render(request, "post_detail.html", context)

@login_required
def delete_post(request, post_id):
    Post.objects.delete(id=post_id)
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
        'message': 'The post and all related comments were successfully erased',
    }
    return redirect("message.html", context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
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
    Comment.objects.create(post=post, content=comment_content, created_by=request.user)
    return redirect(post_detail, post_id)

# search engine

@login_required
def search_results(request):
    search_text = request.POST.get("search_text", "")
    found_users = User.objects.filter(username__icontains=search_text)
    posts = Post.objects.filter(content__icontains=search_text)
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
        'search_text': search_text,
        'found_users': found_users,
        'posts': posts
    }
    return render(request, "search_results.html", context)

# user interface

@login_required
def get_my_friends(request):
    friendships = Friendship.objects.filter(
        Q(from_user_id=request.user.id)
        | Q(to_user_id=request.user.id)
        & Q(is_active=True)
    )
    friend_id_list=[]
    for friendship in friendships:
        if friendship.to_user_id != request.user.id:
            friend_id_list.append(friendship.to_user_id)
        else:
            friend_id_list.append(friendship.from_user_id)
    people = User.objects.filter(id__in=friend_id_list)
    return people

@login_required
def message(request, message):
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
        'message': message,
    }
    return render(request, "message.html", context)

# friendship management

@login_required
def send_friendship_request(request, to_user_id):
    my_id = request.user.id
    # to_user_id = request.POST.get('to_user_id', '')
    Friendship.objects.create(from_user_id=my_id, to_user_id=to_user_id)
    context = {
        'message': 'your friendship request was sent'
    }
    return render(request, "message.html", context)

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
    # my_id = request.user.id
    # to_user_id = request.POST.get('to_user_id', '')
    friendship_to_remove = get_friendship_with_user(request, to_user_id)
    friendship_to_remove.delete()
    context = {
        'message': 'your friendship request was sent'
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
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
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
def notifications(request):
    friendship_requests = Friendship.objects.filter(
        is_active=False,
        to_user_id=request.user.id,
    )
    received_comments = Comment.objects.filter(
        ~Q(created_by=request.user),
        post__created_by=request.user
    )
    my_friends_list=get_my_friends(request)
    context = {
        'my_friends_list':my_friends_list,
        'friendship_requests': friendship_requests,
        'received_comments': received_comments,
    }
    return render(request, 'notifications.html', context)