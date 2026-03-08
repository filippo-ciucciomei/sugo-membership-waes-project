from django.shortcuts import render
from django.utils import timezone
from .models import MembershipPurchase
from django.shortcuts import render

# Create your views here.

def user_has_active_membership(user):
    if not user.is_authenticated:
        return False

    return MembershipPurchase.objects.filter(
        user=user,
        expiry_date__gte=timezone.now().date()
    ).exists()

# This view renders a page informing the user that they need an active membership to access certain features.
def membership_required(request):
    return render(request, "membership/membership_required.html")