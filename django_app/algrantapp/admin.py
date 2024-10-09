from django.contrib import admin
from .models import Post, Comment, Friendship, Conversation, Message

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friendship)
admin.site.register(Conversation)
admin.site.register(Message)