from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete

from rides.models import Ride, Attendance, Comment
from .models import Notification

User = get_user_model()

# When a new ride is created, notify all users except the creator
@receiver(post_save, sender=Ride)
def ride_created_notification(sender, instance, created, **kwargs):
    if created:
        users = User.objects.exclude(id=instance.user.id)
        for user in users:
            Notification.objects.create(
                recipient=user,
                actor=instance.user,
                ride=instance,
                type=Notification.RIDE_CREATED
            )

# When a user joins a ride, notify the ride creator (unless they joined their own ride)
@receiver(post_save, sender=Attendance)
def ride_joined_notification(sender, instance, created, **kwargs):
    if created:
        ride_creator = instance.ride.user
        joining_user = instance.user
        if ride_creator != joining_user:
            Notification.objects.create(
                recipient=ride_creator,
                actor=joining_user,
                ride=instance.ride,
                type=Notification.RIDE_JOINED
            )

# (Commented out) When a user leaves a ride, notify the ride creator
# See note in code for why this is disabled for now

# When a user comments on a ride, notify the ride creator (unless they commented on their own ride)
@receiver(post_save, sender=Comment)
def ride_comment_notification(sender, instance, created, **kwargs):
    if created:
        ride_creator = instance.ride.user
        commenting_user = instance.user
        if ride_creator != commenting_user:
            Notification.objects.create(
                recipient=ride_creator,
                actor=commenting_user,
                ride=instance.ride,
                type=Notification.RIDE_COMMENT
            )

# When a user comments, notify other previous commenters (except the ride creator and themselves)
@receiver(post_save, sender=Comment)
def other_commenters_notification(sender, instance, created, **kwargs):
    if created:
        commenting_user = instance.user
        ride_creator_id = instance.ride.user.id
        previous_commenters = (
            Comment.objects
            .filter(ride=instance.ride)
            .exclude(user=commenting_user)
            .exclude(user_id=ride_creator_id)
            .values_list("user", flat=True).distinct()
        )
        for commenter_id in previous_commenters:
            Notification.objects.create(
                recipient_id=commenter_id,
                actor=commenting_user,
                ride=instance.ride,
                type=Notification.RIDE_COMMENT
            )