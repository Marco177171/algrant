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
    seen = models.BooleanField(default=False)
    def __str__(self):
        return self.content

class Friendship (models.Model):
    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()
    is_active = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return str(self.from_user_id) + str(self.to_user_id)

# notifications

class Notification (models.Model):
    content = models.CharField(max_length=256)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return self.content

class PushSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    endpoint = models.TextField()
    expiration_time = models.DateTimeField(null=True, blank=True)
    p256dh = models.TextField()
    auth = models.TextField()

class Conversation(models.Model):
    admin_id = models.IntegerField()
    conversation_name = models.TextField(max_length=128, default='chat')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.conversation_name

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=2048)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return self.content
    
class Sponsor(models.Model):
<<<<<<< HEAD
    name = models.TextField(max_length=64)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slogan = models.TextField(max_length=256)
    url_to_website = models.URLField(max_length=256)
    activated_on = models.DateTimeField(auto_now_add=True)
    days_of_validity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
=======
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.TextField(max_length=128)
    slogan = models.TextField(max_length=256)
    website_url = models.URLField()
    valid_through = models.DateTimeField()
    def __str__(self):
        return self.name
>>>>>>> dev
