from time import timezone
from django.conf import settings
from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class RSVP(models.Model):
    STATUS_CHOICES = [
        ("yes", "Attending"),
        ("maybe", "Maybe"),
        ("no", "Not Attending"),
    ]

    event = models.ForeignKey(Event, related_name="rsvps", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="maybe")

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user.username} → {self.event.title} ({self.status})"
