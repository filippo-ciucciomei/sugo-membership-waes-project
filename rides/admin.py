from django.contrib import admin
from .models import Ride, Attendance, Comment

# Register your models here.

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "date", "time", "discipline", "user")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("user", "ride", "joined_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "ride", "created_at")
    search_fields = ("user__username", "ride__title", "content")
    list_filter = ("created_at", "user__username", "ride__title")