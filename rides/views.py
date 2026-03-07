from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Ride, Attendance
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

def home(request):
    return render(request, "home.html")

class RideListView(ListView):
    model = Ride
    template_name = "rides/ride_list.html"
    context_object_name = "rides"

    def get_queryset(self):
        today = timezone.now().date()
        return Ride.objects.filter(date__gte=today).order_by("date", "time")


class RideDetailView(DetailView):
    model = Ride
    template_name = "rides/ride_detail.html"
    context_object_name = "ride"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride = self.get_object()

        if self.request.user.is_authenticated:
            context["already_joined"] = Attendance.objects.filter(
                user=self.request.user,
                ride=ride
            ).exists()
        else:
            context["already_joined"] = False

        return context


def join_ride(request, slug):
    ride = get_object_or_404(Ride, slug=slug)

    Attendance.objects.get_or_create(
        user=request.user,
        ride=ride
    )

    return redirect("ride_detail", slug=ride.slug)


def leave_ride(request, slug):
    ride = get_object_or_404(Ride, slug=slug)

    Attendance.objects.filter(
        user=request.user,
        ride=ride
    ).delete()

    return redirect("ride_detail", slug=ride.slug)