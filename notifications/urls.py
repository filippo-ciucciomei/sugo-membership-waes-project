from django.urls import path
from .views import mark_notifications_read
from .views import notifications_list


urlpatterns = [
    path("mark-read/", mark_notifications_read, name="mark_notifications_read"),
    path("", notifications_list, name="notifications_list"),
]