from django.contrib import admin
from .models import Post, Comment, Friendship, Conversation, Message, Sponsor

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('created_by', 'content', 'date_time')
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('created_by', 'content', 'post', 'date_time')
admin.site.register(Comment, CommentAdmin)

class FriendshipAdmin(admin.ModelAdmin):
    model = Friendship
    list_display = ('from_user_id', 'to_user_id', 'is_active', 'seen')
admin.site.register(Friendship, FriendshipAdmin)

class ConversationAdmin(admin.ModelAdmin):
    model = Conversation
    list_display = ('conversation_name', 'participants')
admin.site.register(Conversation)

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('sender', 'conversation', 'content')
admin.site.register(Message)

class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ('name', 'slogan', 'website_url', 'valid_through')
admin.site.register(Sponsor)