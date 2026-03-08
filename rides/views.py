from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Ride, Attendance
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import RideForm
from django.urls import reverse_lazy

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


class CreateRideView(CreateView):
    model = Ride
    form_class = RideForm
    template_name = "rides/create_ride.html"
    success_url = reverse_lazy("ride_list")

    def form_valid(self, form):
        # Set the user to the currently logged-in user before saving the form
        form.instance.user = self.request.user 
        return super().form_valid(form)
    

class UpdateRideView(UpdateView):
    model = Ride
    form_class = RideForm
    template_name = "rides/update_ride.html"
    
    def get_success_url(self):
        return reverse_lazy("ride_detail", kwargs={"slug": self.object.slug})
    
    def form_valid(self, form):
        # Ensure that only the owner can update the ride
        if form.instance.user != self.request.user:
            form.add_error(None, "You are not allowed to edit this ride.")
            return self.form_invalid(form)
        return super().form_valid(form)
    
    
class DeleteRideView(DeleteView):
    model = Ride
    template_name = "rides/delete_ride.html"
    success_url = reverse_lazy("ride_list")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)