from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.


# MembershipPlan defines the different membership options available for purchase.
class MembershipPlan(models.Model):
    # Name of the plan (e.g. Annual Membership)
    name = models.CharField(max_length=100, default="Annual Membership")
    # Price in pence (e.g. 1000 = £10.00)
    price = models.PositiveIntegerField()
    # How long the membership lasts (in days)
    duration_days = models.PositiveIntegerField(default=365)
    # Is this plan currently available for purchase?
    is_active = models.BooleanField(default=True)
    # Internal notes for admins (not shown to users)
    internal_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        # Show the plan name in the admin panel
        return self.name

# MembershipPurchase tracks each purchase of a membership plan by a user, including the start and expiry dates, and the price paid.
class MembershipPurchase(models.Model):
    # The user who bought the membership
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="membership_purchases"
    )
    # The plan that was purchased
    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name="purchases"
    )
    # When the membership starts
    start_date = models.DateField(default=timezone.now)
    # When the membership expires
    expiry_date = models.DateField(blank=True, null=True)
    # How much was paid (in pence)
    price_paid = models.PositiveIntegerField(blank=True, null=True)
    # When this purchase was created
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Set price and expiry if not already set
        if not self.price_paid:
            self.price_paid = self.plan.price
        if not self.expiry_date:
            self.expiry_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        # Is this membership still valid?
        return self.expiry_date >= timezone.now().date()

    def __str__(self):
        # Show user and plan in the admin panel
        return f"{self.user.username} - {self.plan.name}"