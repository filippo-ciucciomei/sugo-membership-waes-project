from django.urls import path
from .views import RideListView, RideDetailView, join_ride, leave_ride

urlpatterns = [
    path("", RideListView.as_view(), name="ride_list"),
    path("<slug:slug>/", RideDetailView.as_view(), name="ride_detail"),
    path("<slug:slug>/join/", join_ride, name="join_ride"),
    path("<slug:slug>/leave/", leave_ride, name="leave_ride"),
]