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
        # def clean(self):
        #     cleaned_data = super(CustomUserCreationForm, self).clean()
        #     username = cleaned_data.get("username")
        #     email = cleaned_data.get("email")
        #     usernamed = User.objects.filter(username=username)
        #     emailed = User.objects.filter(email=email)
        #     if usernamed:
        #         raise forms.ValidationError("That username is already taken. Please select another")
        #     if emailed:
        #         raise forms.ValidationError("An account using that email already exists")
        #     return cleaned_data
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
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user==request.user:
        return redirect(profile)
    friendship = Friendship.objects.filter(
        Q(from_user_id=request.user.id, to_user_id=user.id) |
        Q(to_user_id=request.user.id, from_user_id=user.id)
    ).first()
    is_friend=False
    if (friendship and friendship.is_active):
        is_friend=True
    users_post = Post.objects.filter(created_by=user).order_by('-id')
    context = {
        'is_friend': is_friend,
        'user': user,
        'posts': users_post,
    }
    return render(request, 'user_profile.html', context)

# index and posts

@login_required
def index(request):
    posts=Post.objects.order_by('-id')
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
def delete_post(post_id):
    Post.objects.delete(id=post_id)
    context = {
        'message': 'The post and all related comments were successfully erased',
    }
    return redirect("message.html", context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
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
    Comment.objects.create(post=post, content=comment_content, created_by=request.user)
    return redirect(post_detail, post_id)

# search engine

@login_required
def search_results(request):
    search_text = request.POST.get("search_text", "")
    users = User.objects.filter(username__icontains=search_text)
    posts = Post.objects.filter(content__icontains=search_text)
    context = {
        'search_text': search_text,
        'users': users,
        'posts': posts
    }
    return render(request, "search_results.html", context)

# user interface

@login_required
def base(request):
    friendships = Friendship.objects.filter(
        Q(from_user_id=request.user.id)
        | Q(to_user_id=request.user.id)
        & Q(is_active=True)
    )
    context = {
        # 'posts': User.objects.filter(created_by=request.user).order_by('-id'),
        'people_amount': len(friendships),
    }
    return render(request, 'users/profile.html', context)

@login_required
def message(request, message):
    context = {
        'message': message
    }
    return render(request, "message.html", context)