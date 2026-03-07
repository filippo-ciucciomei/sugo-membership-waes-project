from django.contrib import admin
from .models import Ride, Attendance

# Register your models here.

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "date", "time", "discipline", "user")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("user", "ride", "joined_at")