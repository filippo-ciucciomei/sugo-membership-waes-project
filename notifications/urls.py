from django.urls import path
from .views import mark_notifications_read

urlpatterns = [
    path("mark-read/", mark_notifications_read, name="mark_notifications_read"),
]