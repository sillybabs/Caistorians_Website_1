# Create your models here.
from django.db import models
from django.conf import settings

class Photo(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="community/photos/")
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Admin approval

    def __str__(self):
        return f"{self.uploaded_by.username} - {self.caption[:20]}"

class Story(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Admin moderation

    def __str__(self):
        return self.title
