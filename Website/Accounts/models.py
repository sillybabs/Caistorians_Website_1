from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"