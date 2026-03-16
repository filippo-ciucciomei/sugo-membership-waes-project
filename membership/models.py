# membership/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.



# MembershipPlan defines the different membership options available for purchase.
class MembershipPlan(models.Model):
    name = models.CharField(max_length=100, default="Annual Membership")
    price = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField(default=365)
    is_active = models.BooleanField(default=True)
    internal_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# MembershipPurchase tracks each purchase of a membership plan by a user, including the start and expiry dates, and the price paid.
class MembershipPurchase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="membership_purchases"
    )
    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name="purchases"
    )
    start_date = models.DateField(default=timezone.localdate)
    expiry_date = models.DateField(blank=True, null=True)
    price_paid = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.price_paid:
            self.price_paid = self.plan.price
        if not self.expiry_date:
            self.expiry_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.expiry_date >= timezone.now().date()

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"