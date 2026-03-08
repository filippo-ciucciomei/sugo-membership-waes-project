from django.shortcuts import redirect
from django.utils import timezone
from .models import MembershipPurchase


# It checks if the user is authenticated and has an active membership before allowing access to the view.
class MembershipRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        has_active_membership = MembershipPurchase.objects.filter(
            user=request.user,
            expiry_date__gte=timezone.now().date()
        ).exists()

        if not has_active_membership:
            return redirect("membership_required")

        return super().dispatch(request, *args, **kwargs)