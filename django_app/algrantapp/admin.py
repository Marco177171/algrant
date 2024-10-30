from django.contrib import admin
from .models import Post, Comment, Friendship, PushSubscription, Notification, Conversation, Message, Sponsor

# POSTS

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'created_by', 'content', 'date_time')
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('id', 'created_by', 'content', 'post', 'date_time')
admin.site.register(Comment, CommentAdmin)

# COMMUNITY

class FriendshipAdmin(admin.ModelAdmin):
    model = Friendship
    list_display = ('id', 'from_user_id', 'to_user_id', 'is_active', 'seen')
admin.site.register(Friendship, FriendshipAdmin)

# CHATS

class ConversationAdmin(admin.ModelAdmin):
    model = Conversation
    list_display = ('id', 'conversation_name', 'participants')
admin.site.register(Conversation)

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('id', 'sender', 'conversation', 'content')
admin.site.register(Message)

# USER UPDATES

class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('id', 'content', 'seen')
admin.site.register(Notification)

class PushSubscriptionAdmin(admin.ModelAdmin):
    model = PushSubscription
    list_display = ('id', 'user', 'endpoint', 'expiration_time', 'p256dh', 'auth')
admin.site.register(PushSubscription)

# SUPPORTERS

class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    list_display = ('id', 'name', 'slogan', 'website_url', 'valid_through')
admin.site.register(Sponsor)