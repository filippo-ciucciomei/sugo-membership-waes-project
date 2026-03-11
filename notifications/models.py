from django.db import models
from django.conf import settings
from rides.models import Ride

# Create your models here.

# recipient: the user who receives the notification
# actor: the user who triggered the notification (e.g., the user who joined the ride)
class Notification(models.Model):

    RIDE_CREATED = "ride_created"
    RIDE_JOINED = "ride_joined"
    RIDE_LEFT = "ride_left"
    RIDE_COMMENT = "ride_comment"

    NOTIFICATION_TYPES = [
        (RIDE_CREATED, "Ride created"),
        (RIDE_JOINED, "Ride joined"),
        (RIDE_LEFT, "Ride left"),
        (RIDE_COMMENT, "Ride comment"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="triggered_notifications"
    )
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES
        )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.actor} -> {self.recipient} ({self.type})"