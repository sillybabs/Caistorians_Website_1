# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class ChatRoom(models.Model):
    year_group = models.IntegerField(unique=True)

    def __str__(self):
        return f"Year {self.year_group}"

class MessageeToGroup(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"
