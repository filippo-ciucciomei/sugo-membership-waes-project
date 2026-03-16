from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from notifications.models import Notification
from rides.models import Ride


class TestNotificationModel(TestCase):

    def test_notification_creation(self):
        recipient = User.objects.create_user(
            username="recipient",
            password="testpass123"
        )
        actor = User.objects.create_user(
            username="actor",
            password="testpass123"
        )

        ride = Ride.objects.create(
            user=actor,
            title="Morning Ride",
            description="Fast laps",
            date=date(2026, 4, 10),
            time="07:00",
            max_riders=10,
            discipline="road",
        )

        notification = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            ride=ride,
            type=Notification.RIDE_CREATED,
        )

        self.assertEqual(notification.recipient, recipient)
        self.assertEqual(notification.actor, actor)
        self.assertEqual(notification.ride, ride)
        self.assertEqual(notification.type, Notification.RIDE_CREATED)