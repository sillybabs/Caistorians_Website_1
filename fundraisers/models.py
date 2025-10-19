from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

class Fundraiser(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_raised = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Payment(models.Model):
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=255)
    succeeded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
