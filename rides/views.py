# rides/views.py

# Import Django modules for handling HTTP requests, rendering templates, and working with class-based views
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from django.utils import timezone
# Import models for rides, attendance, and comments
from .models import Ride, Attendance, Comment
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Import forms for creating and editing rides and comments
from .forms import RideForm
from django.urls import reverse_lazy
# Import mixin to require membership for certain views
from membership.mixins import MembershipRequiredMixin
from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_GET



# Create your views here.


# Show the home page
def home(request):
    return render(request, "home.html")


# List all upcoming rides (requires membership)
class RideListView(MembershipRequiredMixin, ListView):
    model = Ride
    template_name = "rides/ride_list.html"
    context_object_name = "rides"

    def get_queryset(self):
        today = timezone.now().date()
        # Only show rides that are today or in the future
        return Ride.objects.filter(date__gte=today).order_by("date", "time")



# Show details for a single ride (requires membership)
class RideDetailView(MembershipRequiredMixin, DetailView):
    model = Ride
    template_name = "rides/ride_detail.html"
    context_object_name = "ride"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride = self.get_object()
        # Add a blank comment form and all comments for this ride
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.all()

        # Check if the user has already joined this ride
        if self.request.user.is_authenticated:
            context["already_joined"] = Attendance.objects.filter(
                user=self.request.user,
                ride=ride
            ).exists()
        else:
            context["already_joined"] = False

        return context
    
    # Handle POST requests for submitting comments
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.ride = self.object
            comment.save()
            return redirect("ride_detail", slug=self.object.slug)

        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)


# Add the current user to the ride's attendance list
def join_ride(request, slug):
    ride = get_object_or_404(Ride, slug=slug)

    Attendance.objects.get_or_create(
        user=request.user,
        ride=ride
    )

    return redirect("ride_detail", slug=ride.slug)


# Remove the current user from the ride's attendance list
def leave_ride(request, slug):
    ride = get_object_or_404(Ride, slug=slug)

    Attendance.objects.filter(
        user=request.user,
        ride=ride
    ).delete()

    return redirect("ride_detail", slug=ride.slug)



# View for creating a new ride (requires membership)
class CreateRideView(MembershipRequiredMixin, CreateView):
    model = Ride
    form_class = RideForm
    template_name = "rides/create_ride.html"
    success_url = reverse_lazy("ride_list")

    def form_valid(self, form):
        # Set the user to the currently logged-in user before saving the form
        form.instance.user = self.request.user 
        return super().form_valid(form)


# View for updating an existing ride (only the owner can edit)
class UpdateRideView(MembershipRequiredMixin, UpdateView):
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


# View for deleting a ride (only the owner can delete)
class DeleteRideView(MembershipRequiredMixin, DeleteView):
    model = Ride
    template_name = "rides/delete_ride.html"
    success_url = reverse_lazy("ride_list")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)



# View for editing a comment (only the author can edit)
class UpdateCommentView(MembershipRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "rides/edit_comment.html"

    def get_success_url(self):
        return reverse_lazy(
            "ride_detail",
            kwargs={"slug": self.object.ride.slug}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ride"] = self.object.ride
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Only allow the comment author to edit their comment
        if self.object.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)



# View for deleting a comment (only the author can delete)
class DeleteCommentView(MembershipRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        # Redirect back to the ride detail page
        return reverse_lazy(
            "ride_detail",
            kwargs={"slug": self.object.ride.slug}
        )

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Only allow the comment author to delete their comment
        if self.object.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Skip confirmation page and delete directly
        return self.delete(request, *args, **kwargs)
