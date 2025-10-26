from django.db import models
from django.conf import settings

class GroupChatRoom(models.Model):
    cohort_year = models.IntegerField(unique=True)

    def __str__(self):
        return f"Cohort {self.cohort_year}"

class GroupMessage(models.Model):
    room = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"
