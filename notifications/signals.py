from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete


from rides.models import Ride, Attendance, Comment
from .models import Notification


User = get_user_model()

# signal to create notifications when a new ride is created
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



# signal to create notifications when a user joins a ride
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


# REMOVING THIS SIGNAL FOR NOW TO AVOID ISSUES WITH DELETING RIDES
# fix for the future: add the notification to the ride view

# # signal to create notifications when a user leaves a ride
# @receiver(post_delete, sender=Attendance)
# def ride_left_notification(sender, instance, **kwargs):

#     if not Ride.objects.filter(id=instance.ride_id).exists():
#         return

#     ride_creator = instance.ride.user
#     leaving_user = instance.user

#     if ride_creator != leaving_user:
#         Notification.objects.create(
#             recipient=ride_creator,
#             actor=leaving_user,
#             ride=instance.ride,
#             type=Notification.RIDE_LEFT
#         )



# signal to create notifications when a user comments on a ride
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

# signal to create notifications for other commenters when a new comment is added to a ride
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