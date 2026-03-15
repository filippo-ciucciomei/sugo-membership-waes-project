from django.db import models
from django.conf import settings
from rides.models import Ride

# Create your models here.


# Notification model: stores notifications for users about ride activity
class Notification(models.Model):

    # Notification type constants
    RIDE_CREATED = "ride_created"
    RIDE_JOINED = "ride_joined"
    RIDE_LEFT = "ride_left"
    RIDE_COMMENT = "ride_comment"

    # Choices for the type field
    NOTIFICATION_TYPES = [
        (RIDE_CREATED, "Ride created"),
        (RIDE_JOINED, "Ride joined"),
        (RIDE_LEFT, "Ride left"),
        (RIDE_COMMENT, "Ride comment"),
    ]

    # The user who receives the notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    # The user who triggered the notification (e.g. joined a ride)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="triggered_notifications"
    )
    # The ride this notification is about
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    # What type of notification is this?
    type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES
        )
    # Has the user read this notification?
    is_read = models.BooleanField(default=False)
    # When the notification was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Show newest notifications first
        ordering = ["-created_at"]

    def __str__(self):
        # Show a readable summary in the admin panel
        return f"{self.actor} -> {self.recipient} ({self.type})"