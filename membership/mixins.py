from django.shortcuts import redirect
from django.utils import timezone
from .models import MembershipPurchase

# Mixin to require an active membership for a view
class MembershipRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # If the user is not logged in, send them to the login page
        if not request.user.is_authenticated:
            return redirect("account_login")

        # Check if the user has an active (not expired) membership
        has_active_membership = MembershipPurchase.objects.filter(
            user=request.user,
            expiry_date__gte=timezone.now().date()
        ).exists()

        # If not, send them to the membership required page
        if not has_active_membership:
            return redirect("membership_required")

        # Otherwise, let them access the view
        return super().dispatch(request, *args, **kwargs)