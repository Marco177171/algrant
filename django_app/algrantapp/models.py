from django.db import models
from django.conf import settings

# Create your models here.

class Post (models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=512)
    def __str__(self):
        return self.content

class Comment (models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=512)
    def __str__(self):
        return self.content

class Friendship (models.Model):
    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return str(self.from_user_id) + str(self.to_user_id)
    
class Notification (models.Model):
    content = models.CharField(max_length=256)
    def __str__(self):
        return self.content

class Conversation(models.Model):
    conversation_name = models.TextField(max_length=128, default='chat')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.conversation_name

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content