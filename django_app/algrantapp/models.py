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