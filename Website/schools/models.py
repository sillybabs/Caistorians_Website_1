from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="school_logos/", blank=True, null=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name