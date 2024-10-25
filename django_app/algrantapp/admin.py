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

class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ('name', 'is_active', 'created_by', 'url_to_website', 'slogan')
admin.site.register(Sponsor, SponsorAdmin)

class ConversationAdmin(admin.ModelAdmin):
    model = Conversation
    list_display = ('conversation_name', 'admin_id')
admin.site.register(Conversation)

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('sender', 'content', 'conversation', 'timestamp')
admin.site.register(Message, MessageAdmin)