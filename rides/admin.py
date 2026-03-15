from django.contrib import admin
from .models import Ride, Attendance, Comment

# Register your models here.

# Admin panel settings for Ride
@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ("title", "slug", "date", "time", "discipline", "user")

# Admin panel settings for Attendance
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ("user", "ride", "joined_at")

# Admin panel settings for Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ("user", "ride", "created_at")
    # Allow searching by username, ride title, or comment content
    search_fields = ("user__username", "ride__title", "content")
    # Add filters for creation date, username, and ride title
    list_filter = ("created_at", "user__username", "ride__title")