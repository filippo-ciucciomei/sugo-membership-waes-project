from django.urls import path
from .views import membership_required

urlpatterns = [
    path("", membership_required, name="membership_required"),
]