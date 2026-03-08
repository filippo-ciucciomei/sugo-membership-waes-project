from django.urls import path
from .views import RideListView, RideDetailView, join_ride, leave_ride, CreateRideView, UpdateRideView, DeleteRideView

urlpatterns = [
    path("", RideListView.as_view(), name="ride_list"),
    path("create/", CreateRideView.as_view(), name="create_ride"),
    path("<slug:slug>/", RideDetailView.as_view(), name="ride_detail"),
    path("<slug:slug>/join/", join_ride, name="join_ride"),
    path("<slug:slug>/leave/", leave_ride, name="leave_ride"),
    path("<slug:slug>/edit/", UpdateRideView.as_view(), name="update_ride"),
    path("<slug:slug>/delete/", DeleteRideView.as_view(), name="delete_ride"),
]