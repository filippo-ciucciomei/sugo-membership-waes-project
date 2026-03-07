from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


# Create your models here.

# change the deleted user name to deleted_user in the database
def get_deleted_user():
    User = get_user_model()
    deleted_user, created = User.objects.get_or_create(
        username="deleted_user",
        defaults={"email": "deleted_user@example.com"},
    )
    return deleted_user.pk

class Ride(models.Model):
    DISCIPLINE_CHOICES = [
        ("road", "Road"),
        ("gravel", "Gravel"),
        ("mtb", "MTB"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=get_deleted_user,    
        related_name="rides"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    max_riders = models.PositiveIntegerField()
    discipline = models.CharField(max_length=20, choices=DISCIPLINE_CHOICES)
    gpx_file = models.FileField(upload_to="gpx/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # preview the object in admin panel
    def __str__(self):
        return f"{self.title} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)  # first save to get ID
            self.slug = f"{slugify(self.title)}-{self.id}"
        super().save(*args, **kwargs)



class Attendance(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name="attendances"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "ride")