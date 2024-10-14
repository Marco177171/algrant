from django.contrib import admin
from .models import Post, Comment, Friendship, Conversation, Message

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('created_by', 'content', 'date_time')
    # list_editable = ('created_by', 'content', 'date_time') 
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('created_by', 'content', 'post', 'date_time')
    # list_editable = ('created_by', 'content', 'post', 'date_time')
admin.site.register(Comment, CommentAdmin)

class FriendshipAdmin(admin.ModelAdmin):
    model = Friendship
    list_display = ('from_user_id', 'to_user_id', 'is_active', 'seen')
    # list_editable = ('from_user_id', 'to_user_id', 'is_active', 'seen')
admin.site.register(Friendship, FriendshipAdmin)

admin.site.register(Conversation)
admin.site.register(Message)