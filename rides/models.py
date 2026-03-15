from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


# Create your models here.


# Helper function: get or create a special user for deleted accounts
def get_deleted_user():
    User = get_user_model()
    deleted_user, created = User.objects.get_or_create(
        username="deleted_user",
        defaults={"email": "deleted_user@example.com"},
    )
    return deleted_user.pk


# Ride model: represents a group ride event
class Ride(models.Model):
    # What type of ride is this?
    DISCIPLINE_CHOICES = [
        ("road", "Road"),
        ("gravel", "Gravel"),
        ("mtb", "MTB"),
    ]

    # The user who created the ride
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=get_deleted_user,    
        related_name="rides"
    )
    # Title of the ride
    title = models.CharField(max_length=200)
    # Unique slug for URLs
    slug = models.SlugField(unique=True, blank=True, editable=False)
    # Description of the ride
    description = models.TextField(blank=True)
    # Date and time of the ride
    date = models.DateField()
    time = models.TimeField()
    # Maximum number of riders allowed
    max_riders = models.PositiveIntegerField()
    # Type of ride (road, gravel, mtb)
    discipline = models.CharField(max_length=20, choices=DISCIPLINE_CHOICES)
    # Optional GPX file for the route
    gpx_file = models.FileField(upload_to="gpx/", blank=True, null=True)
    # When the ride was created/updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Show a readable name in the admin panel
    def __str__(self):
        return f"{self.title} - {self.date}"

    def save(self, *args, **kwargs):
        # Automatically generate a slug if not set
        if not self.slug:
            super().save(*args, **kwargs)  # first save to get ID
            self.slug = f"{slugify(self.title)}-{self.id}"
        super().save(*args, **kwargs)




# Attendance model: tracks which users have joined which rides
class Attendance(models.Model):
    # The user who joined the ride
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    # The ride they joined
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    # When they joined
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Each user can only join a ride once
        unique_together = ("user", "ride")




# Comment model: stores comments left by users on rides
class Comment(models.Model):
    # The user who wrote the comment
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=get_deleted_user,    
        related_name="comments"
    )
    # The ride the comment is about
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    # The text of the comment
    content = models.TextField()
    # When the comment was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Show comments in order of creation
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.ride}"